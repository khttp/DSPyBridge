"""
ReAct agent endpoint for intelligent tool usage
"""
from datetime import datetime
from fastapi import APIRouter, HTTPException

from app.core import setup_logging
from app.models import ReActRequest, ReActResponse
from app.services import dspy_service
from app.tools import get_joke_from_api, is_joke_request

logger = setup_logging()
router = APIRouter()


@router.post("/react", response_model=ReActResponse)
async def react_chat(request: ReActRequest):
    """
    ReAct (Reasoning + Acting) endpoint that can use tools.
    Analyzes user message and decides whether to use tools or respond directly.
    """
    try:
        # Handle fallback when DSPy is not configured
        if not dspy_service.configured or dspy_service.react_agent is None:
            return await _handle_fallback_react(request)
        
        # If tools are disabled, use regular chat
        if not request.enable_tools:
            result = dspy_service.chat_module(message=request.message)
            return ReActResponse(
                response=result.response,
                message=request.message,
                tool_used=None,
                tool_result=None,
                timestamp=datetime.now(),
                model_used=dspy_service.model_provider
            )
        
        # Use ReAct agent to decide on action
        available_tools = "joke_api: Get a random joke when user wants to laugh or asks for jokes"
        
        react_result = dspy_service.react_agent(
            message=request.message,
            available_tools=available_tools
        )
        
        # Check if agent decided to use joke tool
        tool_used = None
        tool_result = None
        final_response = react_result.response
        
        if _should_use_joke_tool(react_result.action, request.message):
            tool_used = "joke_api"
            tool_result = await get_joke_from_api()
            final_response = _format_joke_response(tool_result, react_result.thought)
        
        return ReActResponse(
            response=final_response,
            message=request.message,
            tool_used=tool_used,
            tool_result=tool_result,
            timestamp=datetime.now(),
            model_used=dspy_service.model_provider
        )
        
    except Exception as e:
        logger.error(f"ReAct error: {e}")
        raise HTTPException(status_code=500, detail=f"ReAct processing failed: {str(e)}")


async def _handle_fallback_react(request: ReActRequest) -> ReActResponse:
    """Handle ReAct when DSPy is not configured"""
    if is_joke_request(request.message):
        joke_result = await get_joke_from_api()
        response = _format_joke_response(joke_result)
        
        return ReActResponse(
            response=response,
            message=request.message,
            tool_used="joke_api",
            tool_result=joke_result,
            timestamp=datetime.now(),
            model_used="Fallback (DSPy not configured)"
        )
    else:
        return ReActResponse(
            response="DSPy is not properly configured. Please check your setup.",
            message=request.message,
            tool_used=None,
            tool_result=None,
            timestamp=datetime.now(),
            model_used="Fallback (DSPy not configured)"
        )


def _should_use_joke_tool(action: str, message: str) -> bool:
    """Determine if joke tool should be used"""
    return ("joke" in action.lower() or 
            "joke_api" in action.lower() or 
            is_joke_request(message))


def _format_joke_response(joke_result: dict, thought: str = None) -> str:
    """Format the joke response"""
    if joke_result["success"]:
        joke = joke_result["joke"]
        response = f"Here's a {joke['type']} joke for you:\n\n{joke['setup']}\n{joke['punchline']}"
        if thought:
            response += f"\n\nThought process: {thought}"
        return response
    else:
        fallback = joke_result.get("fallback_joke", {})
        return f"Here's a backup joke:\n\n{fallback.get('setup', 'Error')}\n{fallback.get('punchline', 'Something went wrong!')}"
