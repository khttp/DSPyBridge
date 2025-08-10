"""
Health check endpoint
"""
from datetime import datetime
from fastapi import APIRouter

from app.core import config
from app.models import HealthResponse

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint to verify service status"""
    return HealthResponse(
        status="healthy",
        service=config.APP_NAME,
        version=config.VERSION,
        dspy_configured=config.is_configured,
        model_provider="DSPy ReAct Agent" if config.is_configured else "Not configured",
        timestamp=datetime.now()
    )
