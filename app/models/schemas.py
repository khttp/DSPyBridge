"""
Pydantic models for API requests and responses
"""
from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


# Request Models
class ChatRequest(BaseModel):
    """Request model for basic chat."""
    message: str = Field(..., description="User message")
    max_tokens: int = Field(default=150, ge=1, le=2000, description="Maximum tokens to generate")
    temperature: float = Field(default=0.7, ge=0.0, le=2.0, description="Sampling temperature")


class ReActRequest(BaseModel):
    """Request model for ReAct agent."""
    message: str = Field(..., description="User message")
    enable_tools: bool = Field(default=True, description="Enable tool usage")


class QuestionRequest(BaseModel):
    """Request model for question answering."""
    question: str = Field(..., description="Question to answer")
    context: Optional[str] = Field(default=None, description="Optional context")


class RetrievalRequest(BaseModel):
    """Request model for retrieval-enhanced generation."""
    query: str = Field(..., description="Query for retrieval")
    documents: List[str] = Field(..., description="Documents to search through")
    top_k: int = Field(default=3, ge=1, le=10, description="Number of top documents to retrieve")


# Response Models
class ChatResponse(BaseModel):
    """Response model for chat completion."""
    response: str
    message: str
    timestamp: datetime
    model_used: str


class ReActResponse(BaseModel):
    """Response model for ReAct agent."""
    response: str
    message: str
    tool_used: Optional[str] = None
    tool_result: Optional[Dict[str, Any]] = None
    timestamp: datetime
    model_used: str


class QuestionResponse(BaseModel):
    """Response model for question answering."""
    question: str
    answer: str
    reasoning: Optional[str] = None
    timestamp: datetime


class RetrievalResponse(BaseModel):
    """Response model for retrieval-enhanced generation."""
    query: str
    retrieved_docs: List[str]
    generated_response: str
    retrieval_scores: Optional[List[float]] = None
    timestamp: datetime


class HealthResponse(BaseModel):
    """Response model for health check."""
    status: str
    service: str
    version: str
    dspy_configured: bool
    model_provider: str
    timestamp: datetime
