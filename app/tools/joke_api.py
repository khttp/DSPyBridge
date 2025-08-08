"""
Joke API tool for getting random jokes
"""
import asyncio
import random
from typing import Dict, Any


async def get_joke_from_api() -> Dict[str, Any]:
    """
    Get a random joke from the mock joke API.
    
    In production, this would call a real joke API like:
    - https://icanhazdadjoke.com/
    - https://jokeapi.dev/
    - etc.
    
    Returns:
        Dict containing joke data and metadata
    """
    try:
        # Simulate API call delay
        await asyncio.sleep(0.3)
        
        jokes = [
            {
                "setup": "Why don't scientists trust atoms?",
                "punchline": "Because they make up everything!",
                "type": "science"
            },
            {
                "setup": "What do you call a fake noodle?",
                "punchline": "An impasta!",
                "type": "food"
            },
            {
                "setup": "Why did the scarecrow win an award?",
                "punchline": "He was outstanding in his field!",
                "type": "general"
            },
            {
                "setup": "What do you call a bear with no teeth?",
                "punchline": "A gummy bear!",
                "type": "animal"
            },
            {
                "setup": "Why don't eggs tell jokes?",
                "punchline": "They'd crack each other up!",
                "type": "food"
            }
        ]
        
        selected_joke = random.choice(jokes)
        
        return {
            "success": True,
            "joke": selected_joke,
            "source": "Mock Joke API v1.0"
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "fallback_joke": {
                "setup": "Why did the API break?",
                "punchline": "It couldn't handle the requests!",
                "type": "tech"
            }
        }


def is_joke_request(message: str) -> bool:
    """
    Check if the user message is requesting a joke.
    
    Args:
        message: User message to analyze
        
    Returns:
        True if message contains joke-related keywords
    """
    joke_keywords = ["joke", "funny", "laugh", "humor", "comedy", "amusing"]
    return any(keyword in message.lower() for keyword in joke_keywords)
