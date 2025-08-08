"""
Question answering and reasoning endpoints
"""
from datetime import datetime
from fastapi import APIRouter, HTTPException

from app.core import setup_logging
from app.models import QuestionRequest, QuestionResponse
from app.services import dspy_service

logger = setup_logging()
router = APIRouter()


@router.post("/question", response_model=QuestionResponse)
async def question_answering(request: QuestionRequest):
    """
    Direct question answering using DSPy.
    """
    try:
        if not dspy_service.configured or dspy_service.qa_module is None:
            return QuestionResponse(
                question=request.question,
                answer="DSPy is not properly configured. Please check your setup.",
                timestamp=datetime.now()
            )
        
        result = dspy_service.qa_module(
            question=request.question,
            context=request.context or ""
        )
        
        return QuestionResponse(
            question=request.question,
            answer=result.answer,
            timestamp=datetime.now()
        )
        
    except Exception as e:
        logger.error(f"Question answering error: {e}")
        raise HTTPException(status_code=500, detail=f"Question processing failed: {str(e)}")


@router.post("/reasoning", response_model=QuestionResponse)
async def chain_of_thought_reasoning(request: QuestionRequest):
    """
    Chain of thought reasoning using DSPy.
    """
    try:
        if not dspy_service.configured or dspy_service.cot_qa_module is None:
            return QuestionResponse(
                question=request.question,
                answer="DSPy is not properly configured. Please check your setup.",
                reasoning="Chain of thought reasoning is not available.",
                timestamp=datetime.now()
            )
        
        result = dspy_service.cot_qa_module(
            question=request.question,
            context=request.context or ""
        )
        
        return QuestionResponse(
            question=request.question,
            answer=result.answer,
            reasoning=result.reasoning,
            timestamp=datetime.now()
        )
        
    except Exception as e:
        logger.error(f"Chain of thought error: {e}")
        raise HTTPException(status_code=500, detail=f"Reasoning processing failed: {str(e)}")
