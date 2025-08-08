"""
Health check endpoint
"""
from datetime import datetime
from fastapi import APIRouter

from app.core import config
from app.models import HealthResponse
from app.services import dspy_service

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint to verify service status"""
    return HealthResponse(
        status="healthy",
        service=config.APP_NAME,
        version=config.VERSION,
        dspy_configured=dspy_service.configured,
        model_provider=dspy_service.model_provider,
        timestamp=datetime.now()
    )
