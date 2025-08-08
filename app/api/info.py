"""
API endpoints information
"""
from fastapi import APIRouter

router = APIRouter()


@router.get("/endpoints")
async def list_endpoints():
    """List available endpoints and their usage."""
    return {
        "service": "DSPyBridge API",
        "endpoints": {
            "/react": {
                "method": "POST",
                "description": "ReAct agent with tool usage (recommended for chatbots)",
                "use_case": "Smart chat that can use tools like joke API when appropriate"
            },
            "/chat": {
                "method": "POST",
                "description": "Basic chat endpoint for simple conversations",
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
            "/retrieval": {
                "method": "POST",
                "description": "Retrieval-enhanced generation",
                "use_case": "Query documents and get contextual responses"
            },
            "/health": {
                "method": "GET",
                "description": "Health check and configuration status",
                "use_case": "Check if DSPy and Groq are properly configured"
            }
        },
        "features": {
            "DSPy Integration": "Uses DSPy framework for structured AI programming",
            "Groq LLM": "Fast inference with Groq's language models",
            "ReAct Agent": "Reasoning + Acting agent that can use tools",
            "Tool Integration": "Joke API and extensible tool system",
            "Retrieval Enhancement": "Document retrieval with contextual generation",
            "Chain of Thought": "Step-by-step reasoning capabilities"
        },
        "quick_start": {
            "1": "Set GROQ_API_KEY environment variable",
            "2": "Install: poetry install",
            "3": "Run: uvicorn app.main:app --reload",
            "4": "Test: curl -X POST http://localhost:8000/react -d '{\"message\": \"Tell me a joke!\"}' -H 'Content-Type: application/json'"
        }
    }
