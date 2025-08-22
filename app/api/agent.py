"""
ReAct agent endpoint using DSPy Module classes
"""
from datetime import datetime
from fastapi import APIRouter, HTTPException
import dspy

from app.core import setup_logging, config
from app.models import AgentRequest, AgentResponse
from app.tools import get_default_tools

logger = setup_logging()
router = APIRouter()


class AgentModule(dspy.Module):
    """DSPy Module for ReAct agent with tools"""
    
    def __init__(self, tools):
        super().__init__()
        
        # Initialize ReAct with tools
        self.react = dspy.ReAct(
            signature="user_request -> analysis_response",
            tools=tools,
            max_iters=6
        )
    
    def forward(self, user_request: str) -> dspy.Prediction:
        return self.react(user_request=user_request)


# Global module instance
_agent_module: AgentModule = None
_configured = False


def _ensure_configured():
    """Ensure DSPy is configured"""
    global _configured, _agent_module
    
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
        
        # Initialize agent module with tools
        tools = get_default_tools()
        _agent_module = AgentModule(tools)
        _configured = True
        logger.info("Agent module configured successfully with weather and joke tools")
        
    except Exception as e:
        logger.error(f"Failed to configure agent module: {e}")
        _configured = True


@router.post("/agent", response_model=AgentResponse)
async def agent_chat(request: AgentRequest):
    """
    ReAct agent using DSPy AgentModule with tools.
    Best for: Tasks requiring tools (weather, jokes), reasoning + acting, complex interactions.
    """
    _ensure_configured()
    
    if not config.is_configured:
        return AgentResponse(
            response="Service not configured. Please set GROQ_API_KEY.",
            message=request.message,
            timestamp=datetime.now(),
            model_used="Not configured"
        )
    
    if not _agent_module:
        raise HTTPException(status_code=500, detail="Agent module not initialized")
    
    try:
        # Use DSPy AgentModule for tool-based reasoning
        result = _agent_module(user_request=request.message)
        
        return AgentResponse(
            response=getattr(result, "analysis_response", str(result)),
            message=request.message,
            timestamp=datetime.now(),
            model_used="DSPy AgentModule (ReAct with Tools)",
        )
    except Exception as e:
        logger.error(f"Agent error: {e}")
        raise HTTPException(status_code=500, detail=f"Agent processing failed: {str(e)}")
