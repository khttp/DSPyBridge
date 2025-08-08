"""
Chat endpoints for basic conversation
"""
from datetime import datetime
from fastapi import APIRouter, HTTPException

from app.core import setup_logging
from app.models import ChatRequest, ChatResponse
from app.services import dspy_service

logger = setup_logging()
router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Basic chat endpoint for simple conversations.
    """
    try:
        if not dspy_service.configured or dspy_service.chat_module is None:
            fallback_response = (
                f"I received your message: '{request.message}'. "
                "However, DSPy is not properly configured. "
                "Please check your GROQ_API_KEY environment variable."
            )
            return ChatResponse(
                response=fallback_response,
                message=request.message,
                timestamp=datetime.now(),
                model_used="Fallback (DSPy not configured)"
            )
        
        # Use DSPy chat module
        result = dspy_service.chat_module(message=request.message)
        
        return ChatResponse(
            response=result.response,
            message=request.message,
            timestamp=datetime.now(),
            model_used=dspy_service.model_provider
        )
        
    except Exception as e:
        logger.error(f"Chat error: {e}")
        raise HTTPException(status_code=500, detail=f"Chat processing failed: {str(e)}")
