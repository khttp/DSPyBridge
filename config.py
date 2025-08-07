"""
Configuration settings for the DSPy FastAPI Server.
"""

import os
from typing import Dict, Any
from pydantic import BaseSettings

class Settings(BaseSettings):
    """Application settings."""
    
    # Server settings
    app_name: str = "DSPy API Server"
    debug: bool = False
    host: str = "0.0.0.0"
    port: int = 8000
    
    # DSPy Language Model settings
    default_model: str = "openai/gpt-3.5-turbo"
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    anthropic_api_key: str = os.getenv("ANTHROPIC_API_KEY", "")
    
    # Model configuration
    default_temperature: float = 0.7
    default_max_tokens: int = 150
    default_top_p: float = 1.0
    
    # Optimization settings
    optimization_trials: int = 20
    optimization_timeout: int = 300  # seconds
    
    # Retrieval settings
    default_top_k: int = 3
    max_documents: int = 100
    
    # Logging
    log_level: str = "INFO"
    
    class Config:
        env_file = ".env"

# Model configurations for different providers
MODEL_CONFIGS = {
    "openai": {
        "gpt-3.5-turbo": {
            "model": "openai/gpt-3.5-turbo",
            "max_tokens": 4096,
            "temperature": 0.7,
            "top_p": 1.0
        },
        "gpt-4": {
            "model": "openai/gpt-4",
            "max_tokens": 8192,
            "temperature": 0.7,
            "top_p": 1.0
        },
        "gpt-4-turbo": {
            "model": "openai/gpt-4-turbo",
            "max_tokens": 8192,
            "temperature": 0.7,
            "top_p": 1.0
        }
    },
    "anthropic": {
        "claude-3": {
            "model": "anthropic/claude-3-sonnet-20240229",
            "max_tokens": 4096,
            "temperature": 0.7
        },
        "claude-3-haiku": {
            "model": "anthropic/claude-3-haiku-20240307",
            "max_tokens": 4096,
            "temperature": 0.7
        }
    },
    "local": {
        "ollama": {
            "model": "ollama/llama2",
            "max_tokens": 2048,
            "temperature": 0.7
        }
    }
}

# DSPy signature examples and templates
SIGNATURE_TEMPLATES = {
    "basic_qa": {
        "description": "Basic question answering",
        "input_fields": ["question"],
        "output_fields": ["answer"],
        "example": "Question: What is the capital of France? -> Answer: Paris"
    },
    "chain_of_thought": {
        "description": "Step-by-step reasoning",
        "input_fields": ["question"],
        "output_fields": ["reasoning", "answer"],
        "example": "Question: What is 2+2? -> Reasoning: I need to add 2 and 2 together -> Answer: 4"
    },
    "summarization": {
        "description": "Text summarization",
        "input_fields": ["text"],
        "output_fields": ["summary"],
        "example": "Text: Long article... -> Summary: Brief summary..."
    },
    "classification": {
        "description": "Text classification",
        "input_fields": ["text"],
        "output_fields": ["category", "confidence"],
        "example": "Text: This movie was great! -> Category: Positive, Confidence: 0.9"
    },
    "translation": {
        "description": "Language translation",
        "input_fields": ["text", "source_language", "target_language"],
        "output_fields": ["translation"],
        "example": "Text: Hello, Source: English, Target: Spanish -> Translation: Hola"
    },
    "few_shot": {
        "description": "Few-shot learning",
        "input_fields": ["examples", "task_description", "input"],
        "output_fields": ["output"],
        "example": "Examples: [...], Task: Sentiment analysis, Input: Great movie! -> Output: Positive"
    }
}

# Evaluation metrics configuration
EVALUATION_METRICS = {
    "accuracy": {
        "description": "Fraction of correct predictions",
        "function": "accuracy_score"
    },
    "precision": {
        "description": "Precision score for classification",
        "function": "precision_score"
    },
    "recall": {
        "description": "Recall score for classification",
        "function": "recall_score"
    },
    "f1": {
        "description": "F1 score for classification",
        "function": "f1_score"
    },
    "bleu": {
        "description": "BLEU score for text generation",
        "function": "bleu_score"
    },
    "rouge": {
        "description": "ROUGE score for summarization",
        "function": "rouge_score"
    }
}

# Create settings instance
settings = Settings()
