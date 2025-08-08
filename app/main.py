"""
DSPyBridge - Main FastAPI application
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core import config, setup_logging
from app.api import (
    health_router, chat_router, react_router, 
    qa_router, retrieval_router, info_router
)

# Setup logging
logger = setup_logging()

# Create FastAPI app
app = FastAPI(
    title=config.APP_NAME,
    description="A FastAPI server that uses DSPy with Groq, ReAct agents, and tool integration",
    version=config.VERSION,
    docs_url="/docs",
    redoc_url="/redoc"
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
app.include_router(react_router, tags=["ReAct"])
app.include_router(chat_router, tags=["Chat"])
app.include_router(qa_router, tags=["Q&A"])
app.include_router(retrieval_router, tags=["Retrieval"])
app.include_router(info_router, tags=["Info"])


@app.on_event("startup")
async def startup_event():
    """Log startup information"""
    logger.info(f"Starting {config.APP_NAME} v{config.VERSION}")
    logger.info(f"DSPy configured: {config.is_configured}")
    logger.info(f"Running on {config.HOST}:{config.PORT}")


@app.on_event("shutdown")
async def shutdown_event():
    """Log shutdown information"""
    logger.info(f"Shutting down {config.APP_NAME}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=config.HOST,
        port=config.PORT,
        reload=config.DEBUG
    )
