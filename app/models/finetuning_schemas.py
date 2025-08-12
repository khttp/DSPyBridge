"""
Pydantic models for fine-tuning API
"""
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field


class TrainingResponse(BaseModel):
    """Response model for training status"""
    files_processed: List[str]
    examples_count: int
    status: str
    timestamp: datetime


class PredictionRequest(BaseModel):
    """Request model for getting predictions"""
    question: str = Field(..., description="Question to be answered")


class PredictionResponse(BaseModel):
    """Response model for predictions"""
    question: str
    answer: str
    timestamp: datetime
