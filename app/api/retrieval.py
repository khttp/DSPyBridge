"""
RAG (Retrieval-Augmented Generation) endpoint using DSPy Module classes
"""
from datetime import datetime
from fastapi import APIRouter, HTTPException
import dspy
from pathlib import Path
from typing import List, Tuple

from app.core import setup_logging, config
from app.models import RAGRequest, RAGResponse

logger = setup_logging()
router = APIRouter()


class RAGModule(dspy.Module):
    """DSPy Module for Retrieval-Augmented Generation"""
    
    def __init__(self):
        super().__init__()
        
        class RAGSignature(dspy.Signature):
            """Retrieval-augmented generation"""
            query = dspy.InputField(desc="User query")
            context = dspy.InputField(desc="Retrieved document context")
            response = dspy.OutputField(desc="Response based on context")
        
        self.rag_predict = dspy.Predict(RAGSignature)
    
    def forward(self, query: str, context: str) -> dspy.Prediction:
        return self.rag_predict(query=query, context=context)


class DocumentRetriever:
    """Simple document retrieval system"""
    
    def __init__(self, docs_dir: str = "docs"):
        self.docs_directory = Path(docs_dir)
        self.documents: List[str] = []
        self.load_documents()
    
    def load_documents(self):
        """Load documents from docs directory"""
        if not self.docs_directory.exists():
            self.docs_directory.mkdir(exist_ok=True)
            logger.info(f"Created docs directory: {self.docs_directory}")
        
        self.documents = []
        for txt_file in self.docs_directory.glob("*.txt"):
            try:
                with open(txt_file, 'r', encoding='utf-8') as f:
                    content = f.read().strip()
                    if content:
                        self.documents.append(f"[{txt_file.name}] {content}")
                        logger.info(f"Loaded document: {txt_file.name}")
            except Exception as e:
                logger.warning(f"Could not load {txt_file}: {e}")
        
        if not self.documents:
            # Add sample documents if none exist
            sample_docs = [
                "DSPy is a framework for programming language models. It provides structured ways to build AI applications.",
                "ReAct agents combine reasoning and acting to solve complex tasks using tools and external information.",
                "Chain of Thought prompting helps models break down complex problems into step-by-step reasoning."
            ]
            self.documents = sample_docs
            logger.info("No documents found, using sample documents")
        
        logger.info(f"Loaded {len(self.documents)} documents for retrieval")
    
    def retrieve(self, query: str, top_k: int = 3) -> Tuple[List[str], List[float]]:
        """Simple keyword-based document retrieval"""
        if not self.documents:
            return [], []
        
        query_words = set(query.lower().split())
        scores = []
        
        for doc in self.documents:
            doc_words = set(doc.lower().split())
            intersection = len(query_words.intersection(doc_words))
            union = len(query_words.union(doc_words))
            score = intersection / union if union > 0 else 0
            scores.append((doc, score))
        
        # Sort by score and get top-k
        scores.sort(key=lambda x: x[1], reverse=True)
        top_docs = [doc for doc, score in scores[:top_k] if score > 0]
        top_scores = [score for doc, score in scores[:top_k] if score > 0]
        
        return top_docs, top_scores


# Global instances
_rag_module: RAGModule = None
_retriever: DocumentRetriever = None
_configured = False


def _ensure_configured():
    """Ensure DSPy is configured"""
    global _configured, _rag_module, _retriever
    
    if _configured:
        return
    
    # Initialize retriever (works without API key)
    _retriever = DocumentRetriever()
    
    if not config.is_configured:
        _configured = True
        return
    
    try:
        # Configure DSPy
        lm = dspy.LM(
            model=config.DEFAULT_MODEL,
            api_key=config.GROQ_API_KEY,
            max_tokens=config.DEFAULT_MAX_TOKENS,
            temperature=config.DEFAULT_TEMPERATURE
        )
        dspy.configure(lm=lm)
        
        # Initialize RAG module
        _rag_module = RAGModule()
        _configured = True
        logger.info("RAG module configured successfully")
        
    except Exception as e:
        logger.error(f"Failed to configure RAG module: {e}")
        _configured = True


@router.post("/rag", response_model=RAGResponse)
async def rag_query(request: RAGRequest):
    """
    Retrieval-Augmented Generation using DSPy RAGModule.
    Best for: Document-based questions, knowledge base queries, contextual information.
    """
    _ensure_configured()
    
    if not _retriever:
        raise HTTPException(status_code=500, detail="Document retriever not initialized")
    
    try:
        # Retrieve relevant documents
        retrieved_docs, scores = _retriever.retrieve(request.query, request.top_k)
        
        if not retrieved_docs:
            return RAGResponse(
                query=request.query,
                response="No relevant documents found for your query.",
                retrieved_docs=[],
                context_used="",
                timestamp=datetime.now()
            )
        
        # Combine retrieved documents
        context = "\n\n".join(retrieved_docs)
        
        # Generate response
        if config.is_configured and _rag_module:
            # Use DSPy RAGModule for generation
            result = _rag_module(query=request.query, context=context)
            response = result.response
        else:
            # Fallback response without LLM
            response = f"Based on the retrieved documents: {context[:500]}..."
        
        return RAGResponse(
            query=request.query,
            response=response,
            retrieved_docs=retrieved_docs,
            context_used=context,
            timestamp=datetime.now()
        )
        
    except Exception as e:
        logger.error(f"RAG error: {e}")
        raise HTTPException(status_code=500, detail=f"RAG processing failed: {str(e)}")


@router.post("/rag/reload")
async def reload_documents():
    """Reload documents from the docs directory."""
    _ensure_configured()
    
    if not _retriever:
        raise HTTPException(status_code=500, detail="Document retriever not initialized")
    
    try:
        _retriever.load_documents()
        return {
            "message": f"Successfully reloaded {len(_retriever.documents)} documents",
            "timestamp": datetime.now()
        }
    except Exception as e:
        logger.error(f"Document reload error: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to reload documents: {str(e)}")


@router.get("/rag/status")
async def rag_status():
    """Get status of the RAG system."""
    _ensure_configured()
    
    try:
        return {
            "configured": config.is_configured,
            "rag_module_ready": _rag_module is not None,
            "document_count": len(_retriever.documents) if _retriever else 0,
            "docs_directory": str(_retriever.docs_directory) if _retriever else "Not initialized",
            "timestamp": datetime.now()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
