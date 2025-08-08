"""
Retrieval-enhanced generation endpoint
"""
from datetime import datetime
from fastapi import APIRouter, HTTPException

from app.core import setup_logging
from app.models import RetrievalRequest, RetrievalResponse
from app.services import dspy_service

logger = setup_logging()
router = APIRouter()


@router.post("/retrieval", response_model=RetrievalResponse)
async def retrieval_enhanced_generation(request: RetrievalRequest):
    """
    Retrieval-Enhanced (RE) generation using DSPy.
    """
    try:
        if not dspy_service.configured or dspy_service.retrieval_module is None:
            return RetrievalResponse(
                query=request.query,
                retrieved_docs=[],
                generated_response="DSPy is not properly configured. Please check your setup.",
                retrieval_scores=[],
                timestamp=datetime.now()
            )
        
        # Perform retrieval
        retrieved_docs, retrieval_scores = dspy_service.simple_retrieval(
            request.query, 
            request.documents, 
            request.top_k
        )
        
        # Combine retrieved documents as context
        context = "\n\n".join(retrieved_docs) if retrieved_docs else "No relevant documents found."
        
        # Use DSPy retrieval module
        result = dspy_service.retrieval_module(
            query=request.query,
            context=context
        )
        
        return RetrievalResponse(
            query=request.query,
            retrieved_docs=retrieved_docs,
            generated_response=result.response,
            retrieval_scores=retrieval_scores,
            timestamp=datetime.now()
        )
        
    except Exception as e:
        logger.error(f"Retrieval error: {e}")
        raise HTTPException(status_code=500, detail=f"Retrieval processing failed: {str(e)}")
