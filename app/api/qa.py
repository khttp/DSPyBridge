"""
Question answering and reasoning endpoints using DSPy Module classes
"""
from datetime import datetime
from fastapi import APIRouter, HTTPException
import dspy

from app.core import setup_logging, config
from app.models import QuestionRequest, QuestionResponse

logger = setup_logging()
router = APIRouter()



class QuestionModule(dspy.Module):
    """DSPy Module for simple question answering"""
    
    def __init__(self):
        super().__init__()
        
        class QuestionSignature(dspy.Signature):
            """Simple question answering"""
            question = dspy.InputField(desc="User question")
            context = dspy.InputField(desc="Optional context to help answer")
            answer = dspy.OutputField(desc="response as intents and entities")
        
        self.predict = dspy.Predict(QuestionSignature)
    
    def forward(self, question: str,context: str=None) -> dspy.Prediction:
        return self.predict(question=question, context=context)


class ReasoningModule(dspy.Module):
    """DSPy Module for step-by-step reasoning"""
    
    def __init__(self):
        super().__init__()
        class ReasoningSignature(dspy.Signature):
            """Question answering with step-by-step reasoning and context"""
            question = dspy.InputField(desc="user input")
            context = dspy.InputField(desc="Optional context to help reasoning")
            reasoning = dspy.OutputField(desc="Step-by-step reasoning process")
            answer = dspy.OutputField(desc="intents and entities of the user input")
        self.cot = dspy.ChainOfThought(ReasoningSignature)

    def forward(self, question: str, context: str = None) -> dspy.Prediction:
        return self.cot(question=question, context=context)


# Global module instances
_question_module: QuestionModule = None
_reasoning_module: ReasoningModule = None
_configured = False


def _ensure_configured():
    """Ensure DSPy is configured"""
    global _configured, _question_module, _reasoning_module
    
    if _configured:
        return
    
    if not config.is_configured:
        _configured = True
        return
    
    try:
        # Configure DSPy
        # lm = dspy.LM(
        #     model=config.DEFAULT_MODEL,
        #     api_key=config.GROQ_API_KEY,
        #     max_tokens=config.DEFAULT_MAX_TOKENS,
        #     temperature=config.DEFAULT_TEMPERATURE
        # )
        # dspy.configure(lm=lm)
        
        # Initialize modules
        _question_module = QuestionModule()
        _reasoning_module = ReasoningModule()
        _configured = True
        logger.info("QA modules configured successfully")
        
    except Exception as e:
        logger.error(f"Failed to configure QA modules: {e}")
        _configured = True


@router.post("/question", response_model=QuestionResponse)
async def question_answering(request: QuestionRequest):
    """
    Direct question answering using DSPy QuestionModule.
    Best for: Simple Q&A, factual questions, quick answers.
    """
    _ensure_configured()
    
    if not config.is_configured:
        return QuestionResponse(
            question=request.question,
            answer="Service not configured. Please set GROQ_API_KEY.",
            timestamp=datetime.now()
        )
    
    if not _question_module:
        raise HTTPException(status_code=500, detail="Question module not initialized")
    
    try:
        # Use QuestionModule for direct questions
        result = _question_module(question=request.question,context=request.context)
        print(dspy.inspect_history(n=1))
        
        return QuestionResponse(
            question=request.question,
            context=request.context,
            answer=result.answer,
            timestamp=datetime.now()
        )
        
    except Exception as e:
        logger.error(f"Question answering error: {e}")
        raise HTTPException(status_code=500, detail=f"Question processing failed: {str(e)}")


@router.post("/reasoning", response_model=QuestionResponse)
async def chain_of_thought_reasoning(request: QuestionRequest):
    """
    Chain of thought reasoning using DSPy ReasoningModule.
    Best for: Complex problems, step-by-step analysis, detailed explanations.
    """
    _ensure_configured()
    
    if not config.is_configured:
        return QuestionResponse(
            question=request.question,
            answer="Service not configured. Please set GROQ_API_KEY.",
            timestamp=datetime.now()
        )
    
    if not _reasoning_module:
        raise HTTPException(status_code=500, detail="Reasoning module not initialized")
    
    try:
        # Use ReasoningModule for detailed reasoning
        result = _reasoning_module(question=request.question,context=request.context)
        
        return QuestionResponse(
            question=request.question,
            context = request.context,
            answer=result.answer,
            reasoning=result.reasoning,
            timestamp=datetime.now()
        )
        
    except Exception as e:
        logger.error(f"Reasoning error: {e}")
        raise HTTPException(status_code=500, detail=f"Reasoning processing failed: {str(e)}")
