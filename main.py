"""
DSPy FastAPI Server - A server that uses DSPy services with LLM.

This server provides DSPy capabilities including:
- Chat completions using DSPy modules
- Chain of thought reasoning
- Question answering
- Text generation
"""

import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional
import dspy
import logging
from datetime import datetime
from contextlib import asynccontextmanager
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Pydantic models for request/response validation
class ChatRequest(BaseModel):
    """Request model for chat completion."""
    message: str = Field(..., description="User message")
    system_prompt: Optional[str] = Field(default=None, description="Optional system prompt")
    max_tokens: int = Field(default=150, ge=1, le=2000, description="Maximum tokens to generate")
    temperature: float = Field(default=0.7, ge=0.0, le=2.0, description="Sampling temperature")

class ChatResponse(BaseModel):
    """Response model for chat completion."""
    response: str
    message: str
    timestamp: datetime
    model_used: str

class QuestionRequest(BaseModel):
    """Request model for question answering."""
    question: str = Field(..., description="Question to answer")
    context: Optional[str] = Field(default=None, description="Optional context")

class QuestionResponse(BaseModel):
    """Response model for question answering."""
    question: str
    answer: str
    reasoning: Optional[str] = None
    timestamp: datetime

class HealthResponse(BaseModel):
    """Response model for health check."""
    status: str
    dspy_configured: bool
    model_provider: str
    timestamp: datetime

# DSPy Signatures
class BasicChat(dspy.Signature):
    """Basic chat completion signature."""
    message = dspy.InputField(desc="User message")
    response = dspy.OutputField(desc="Assistant response")

class QuestionAnswering(dspy.Signature):
    """Question answering signature."""
    question = dspy.InputField(desc="User question")
    context = dspy.InputField(desc="Relevant context", format=lambda x: x if x else "No additional context provided.")
    answer = dspy.OutputField(desc="Answer to the question")

class ChainOfThoughtQA(dspy.Signature):
    """Chain of thought question answering."""
    question = dspy.InputField(desc="User question")
    context = dspy.InputField(desc="Relevant context", format=lambda x: x if x else "No additional context provided.")
    reasoning = dspy.OutputField(desc="Step-by-step reasoning")
    answer = dspy.OutputField(desc="Final answer")

# Global variables for DSPy modules
chat_module = None
qa_module = None
cot_qa_module = None
dspy_configured = False
model_provider = "Not configured"

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown."""
    global chat_module, qa_module, cot_qa_module, dspy_configured, model_provider
    
    # Startup
    logger.info("Starting DSPy FastAPI Server...")
    
    # Get Groq API key from environment
    groq_api_key = os.getenv("GROQ_API_KEY")
    print(groq_api_key)
    
    if not groq_api_key:
        logger.warning("GROQ_API_KEY not found in environment variables. Using mock responses.")
        model_provider = "Mock (No API Key)"
    else:
        try:
            # Configure DSPy with Groq
            groq_model = dspy.LM(
                model="groq/llama-3.1-8b-instant",
                api_key=groq_api_key,
                max_tokens=500
            )
            
            dspy.configure(lm=groq_model)
            
            # Initialize DSPy modules
            chat_module = dspy.Predict(BasicChat)
            qa_module = dspy.Predict(QuestionAnswering)
            cot_qa_module = dspy.ChainOfThought(ChainOfThoughtQA)
            
            dspy_configured = True
            model_provider = "Groq (llama-3.1-8b-instant)"
            logger.info("DSPy configured successfully with Groq")
            
        except Exception as e:
            logger.error(f"Failed to configure DSPy with Groq: {e}")
            model_provider = f"Failed: {str(e)}"
    
    yield
    
    # Shutdown
    logger.info("Shutting down DSPy FastAPI Server...")

# Initialize FastAPI app
app = FastAPI(
    title="DSPy Chat API Server",
    description="A FastAPI server that uses DSPy with Groq for chat and Q&A",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check endpoint
@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return HealthResponse(
        status="healthy",
        dspy_configured=dspy_configured,
        model_provider=model_provider,
        timestamp=datetime.now()
    )

# Chat endpoint - Main endpoint for chatbot integration
@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Main chat endpoint for chatbot integration.
    Sends user message to DSPy and returns the response.
    """
    try:
        if not dspy_configured or chat_module is None:
            # Fallback response when DSPy is not configured
            fallback_response = f"I received your message: '{request.message}'. However, DSPy is not properly configured with Groq. Please check your GROQ_API_KEY environment variable."
            return ChatResponse(
                response=fallback_response,
                message=request.message,
                timestamp=datetime.now(),
                model_used="Fallback (DSPy not configured)"
            )
        
        # Use DSPy chat module to generate response
        result = chat_module(message=request.message)
        
        return ChatResponse(
            response=result.response,
            message=request.message,
            timestamp=datetime.now(),
            model_used=model_provider
        )
        
    except Exception as e:
        logger.error(f"Chat error: {e}")
        raise HTTPException(status_code=500, detail=f"Chat processing failed: {str(e)}")

# Question answering endpoint
@app.post("/question", response_model=QuestionResponse)
async def question_answering(request: QuestionRequest):
    """
    Question answering endpoint using DSPy.
    Provides direct answers to questions with optional context.
    """
    try:
        if not dspy_configured or qa_module is None:
            fallback_answer = "DSPy is not properly configured. Please check your setup."
            return QuestionResponse(
                question=request.question,
                answer=fallback_answer,
                timestamp=datetime.now()
            )
        
        # Use DSPy QA module
        result = qa_module(
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

# Chain of thought reasoning endpoint
@app.post("/reasoning", response_model=QuestionResponse)
async def chain_of_thought_reasoning(request: QuestionRequest):
    """
    Chain of thought reasoning endpoint using DSPy.
    Provides detailed reasoning along with the answer.
    """
    try:
        if not dspy_configured or cot_qa_module is None:
            fallback_answer = "DSPy is not properly configured. Please check your setup."
            return QuestionResponse(
                question=request.question,
                answer=fallback_answer,
                reasoning="Chain of thought reasoning is not available.",
                timestamp=datetime.now()
            )
        
        # Use DSPy Chain of Thought module
        result = cot_qa_module(
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
        logger.error(f"Chain of thought reasoning error: {e}")
        raise HTTPException(status_code=500, detail=f"Reasoning processing failed: {str(e)}")

# Available endpoints info
@app.get("/endpoints")
async def list_endpoints():
    """List available endpoints and their usage."""
    return {
        "endpoints": {
            "/chat": {
                "method": "POST",
                "description": "Main chat endpoint for chatbot integration",
                "use_case": "Send user messages and get AI responses"
            },
            "/question": {
                "method": "POST", 
                "description": "Direct question answering",
                "use_case": "Get direct answers to questions with optional context"
            },
            "/reasoning": {
                "method": "POST",
                "description": "Chain of thought reasoning",
                "use_case": "Get detailed reasoning along with answers"
            },
            "/health": {
                "method": "GET",
                "description": "Health check and configuration status",
                "use_case": "Check if DSPy and Groq are properly configured"
            }
        },
        "setup_instructions": {
            "1": "Set GROQ_API_KEY environment variable",
            "2": "Install dependencies: poetry install",
            "3": "Run server: uvicorn main:app --reload",
            "4": "Test with: curl -X POST http://localhost:8000/chat -H 'Content-Type: application/json' -d '{\"message\": \"Hello!\"}'"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)