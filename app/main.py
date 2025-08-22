"""
DSPyBridge - Main FastAPI application
"""
import dspy
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core import config, setup_logging
from app.api import (
    health_router, qa_router, info_router, 
    agent_router, upload_router, finetuning_router
    ,retrieval_router
)

import os
# Setup logging
logger = setup_logging()
lm = dspy.LM(
    api_key=config.GROQ_API_KEY,
    model=config.DEFAULT_MODEL,
    temperature=config.DEFAULT_TEMPERATURE,
    max_tokens=config.DEFAULT_MAX_TOKENS
)
# configure dspy with azure openai deployment
# openailm = dspy.LM(
#     model=config.AZURE_OPENAI_DEPLOYMENT,
#     azure_openai_api_key=config.AZURE_OPENAI_API_KEY,
#     azure_openai_base_url=config.AZURE_OPENAI_BASE_URL,
#     azure_openai_version=config.AZURE_OPENAI_VERSION
# )

dspy.configure(lm=lm)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handle startup and shutdown events"""
    # Startup
    logger.info(f"Starting {config.APP_NAME} v{config.VERSION}")
    logger.info(f"DSPy configured: {config.is_configured}")
    logger.info(f"Running on {config.HOST}:{config.PORT}")
    
    yield
    
    # Shutdown
    logger.info(f"Shutting down {config.APP_NAME}")


# Create FastAPI app with lifespan
app = FastAPI(
    title=config.APP_NAME,
    description="A FastAPI server that uses DSPy with Groq, ReAct agents, and tool integration",
    version=config.VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=config.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health_router, tags=["Health"])
app.include_router(qa_router, tags=["Q&A"])
app.include_router(retrieval_router, tags=["RAG"])
app.include_router(info_router, tags=["Info"])
app.include_router(agent_router, tags=["Agent"])
app.include_router(upload_router, tags=["Upload"])
app.include_router(finetuning_router, prefix="/api", tags=["Fine-tuning"])


def run():
    """Start server (production-ish)."""
    import uvicorn
    uvicorn.run(
        app,
        host=config.HOST,
        port=config.PORT,
        reload=False,
    )


def run_dev():
    """Start server in dev with reload and debug logs."""
    import uvicorn
    uvicorn.run(
        app,
        host=config.HOST,
        port=config.PORT,
        reload=True,
        log_level="debug",
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=config.HOST,
        port=config.PORT,
        reload=config.DEBUG
    )
