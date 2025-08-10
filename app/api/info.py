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
            "/agent": {
                "method": "POST",
                "description": "DSPy ReAct agent with weather and joke tools",
                "use_case": "Send messages to an intelligent agent that can use tools"
            },
            "/question": {
                "method": "POST",
                "description": "Direct question answering with optional context",
                "use_case": "Get answers to specific questions"
            },
            "/reasoning": {
                "method": "POST", 
                "description": "Chain of thought reasoning for complex questions",
                "use_case": "Get detailed step-by-step reasoning"
            },
            "/rag": {
                "method": "POST",
                "description": "Retrieval-Augmented Generation from docs/ directory",
                "use_case": "Ask questions about documents in the docs folder"
            },
            "/rag/documents": {
                "method": "GET",
                "description": "List all available documents",
                "use_case": "See what documents are available for RAG queries"
            },
            "/rag/reload": {
                "method": "POST",
                "description": "Reload documents from docs directory",
                "use_case": "Refresh document index after adding new files"
            },
            "/health": {
                "method": "GET",
                "description": "Health check and configuration status",
                "use_case": "Check if service is running and properly configured"
            },
            "/endpoints": {
                "method": "GET",
                "description": "List all available endpoints",
                "use_case": "Discover API capabilities"
            }
        },
        "features": {
            "DSPy ReAct Agent": "Reasoning + Acting agent using DSPy framework",
            "Groq LLM": "Fast inference with Groq's language models",
            "Weather Tool": "Get current weather for any city",
            "Joke Tool": "Get random jokes for entertainment",
            "RAG System": "Retrieval-Augmented Generation from text files",
            "Document Search": "Intelligent document retrieval and Q&A"
        },
        "quick_start": {
            "1": "Set GROQ_API_KEY environment variable",
            "2": "Install: poetry install",
            "3": "Run: poetry run dev",
            "4": "Test: curl -X POST http://localhost:8000/agent -d '{\"message\": \"Tell me a joke!\"}' -H 'Content-Type: application/json'"
        }
    }
