"""
Pydantic models for API requests and responses
"""
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field


# Request Models
class QuestionRequest(BaseModel):
    """Request model for question answering."""
    question: str = Field(..., description="Question to answer")
    context: Optional[str] = Field(default=None, description="Optional context")


class RAGRequest(BaseModel):
    """Request model for RAG queries."""
    query: str = Field(..., description="Query to search documents for")
    top_k: int = Field(default=3, ge=1, le=10, description="Number of top documents to retrieve")


class AgentRequest(BaseModel):
    """Request model for agent interactions."""
    message: str = Field(..., description="User message for the agent")
    max_tokens: int = Field(default=150, ge=1, le=2000, description="Maximum tokens to generate")
    temperature: float = Field(default=0.7, ge=0.0, le=2.0, description="Sampling temperature")


# Response Models
class QuestionResponse(BaseModel):
    """Response model for question answering."""
    question: str
    answer: str
    reasoning: Optional[str] = None
    timestamp: datetime


class AgentResponse(BaseModel):
    """Response model for agent interactions."""
    response: str
    message: str
    timestamp: datetime
    model_used: str


class RAGResponse(BaseModel):
    """Response model for RAG queries."""
    query: str
    response: str
    retrieved_docs: List[str]
    context_used: str
    timestamp: datetime


class HealthResponse(BaseModel):
    """Response model for health check."""
    status: str
    service: str
    version: str
    dspy_configured: bool
    model_provider: str
    timestamp: datetime
