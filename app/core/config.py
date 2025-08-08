"""
Core configuration for DSPyBridge
"""
import os
from typing import Optional
from dotenv import load_dotenv

load_dotenv(override=True)


class Config:
    """Application configuration"""
    
    # Server settings
    APP_NAME: str = "DSPyBridge"
    VERSION: str = "1.0.0"
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    
    # API Keys
    GROQ_API_KEY: Optional[str] = os.getenv("GROQ_API_KEY")
    
    # DSPy/LLM Configuration
    DEFAULT_MODEL: str = os.getenv("DEFAULT_MODEL", "groq/llama-3.1-8b-instant")
    DEFAULT_MAX_TOKENS: int = int(os.getenv("DEFAULT_MAX_TOKENS", "500"))
    DEFAULT_TEMPERATURE: float = float(os.getenv("DEFAULT_TEMPERATURE", "0.7"))
    
    # CORS
    ALLOWED_ORIGINS: list = ["*"]  # Configure for production
    
    @property
    def is_configured(self) -> bool:
        """Check if DSPy can be properly configured"""
        return self.GROQ_API_KEY is not None


config = Config()
