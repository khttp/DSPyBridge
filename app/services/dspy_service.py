"""
DSPy service for managing LLM interactions
"""
import dspy
from typing import Optional, List, Tuple

from app.core import config, setup_logging
from app.models import (
    BasicChat, QuestionAnswering, ChainOfThoughtQA,
    RetrievalEnhanced, ReActAgent
)

logger = setup_logging()


class DSPyService:
    """Service for managing DSPy modules and LLM interactions"""
    
    def __init__(self):
        self.configured = False
        self.model_provider = "Not configured"
        
        # DSPy modules
        self.chat_module: Optional[dspy.Predict] = None
        self.qa_module: Optional[dspy.Predict] = None
        self.cot_qa_module: Optional[dspy.ChainOfThought] = None
        self.retrieval_module: Optional[dspy.Predict] = None
        self.react_agent: Optional[dspy.Predict] = None
        
        self._initialize()
    
    def _initialize(self):
        """Initialize DSPy with configured LLM"""
        if not config.is_configured:
            logger.warning("GROQ_API_KEY not found. Using fallback mode.")
            self.model_provider = "Mock (No API Key)"
            return
        
        try:
            # Configure DSPy with Groq
            groq_model = dspy.LM(
                model=config.DEFAULT_MODEL,
                api_key=config.GROQ_API_KEY,
                max_tokens=config.DEFAULT_MAX_TOKENS
            )
            
            dspy.configure(lm=groq_model)
            
            # Initialize modules
            self.chat_module = dspy.Predict(BasicChat)
            self.qa_module = dspy.Predict(QuestionAnswering)
            self.cot_qa_module = dspy.ChainOfThought(ChainOfThoughtQA)
            self.retrieval_module = dspy.Predict(RetrievalEnhanced)
            self.react_agent = dspy.Predict(ReActAgent)
            
            self.configured = True
            self.model_provider = f"Groq ({config.DEFAULT_MODEL})"
            logger.info("DSPy configured successfully with Groq")
            
        except Exception as e:
            logger.error(f"Failed to configure DSPy: {e}")
            self.model_provider = f"Failed: {str(e)}"
    
    def simple_retrieval(self, query: str, documents: List[str], top_k: int = 3) -> Tuple[List[str], List[float]]:
        """
        Simple keyword-based retrieval.
        In production, use vector embeddings and similarity search.
        """
        scores = []
        query_words = set(query.lower().split())
        
        for doc in documents:
            doc_words = set(doc.lower().split())
            intersection = len(query_words.intersection(doc_words))
            union = len(query_words.union(doc_words))
            score = intersection / union if union > 0 else 0
            scores.append(score)
        
        # Get top-k documents
        doc_scores = list(zip(documents, scores))
        doc_scores.sort(key=lambda x: x[1], reverse=True)
        
        retrieved_docs = [doc for doc, _ in doc_scores[:top_k]]
        retrieval_scores = [score for _, score in doc_scores[:top_k]]
        
        return retrieved_docs, retrieval_scores


# Global service instance
dspy_service = DSPyService()
