"""
Simple joke tool for DSPy agents
"""
import requests


def get_joke_tool() -> str:
    """
    Get a random joke from JokeAPI.
    
    Returns:
        str: A random joke or error message
    """
    try:
        url = "https://sv443.net/jokeapi/v2/joke/Any"
        response = requests.get(url, timeout=15)
        data = response.json()
        
        if data.get("error"):
            return "Sorry, I couldn't fetch a joke right now."
        
        # Handle two-part jokes (setup + delivery)
        if data.get("type") == "twopart":
            setup = data.get("setup", "")
            delivery = data.get("delivery", "")
            if setup and delivery:
                return f"{setup}\n{delivery}"
        
        # Handle single-line jokes
        joke = data.get("joke")
        if joke:
            return joke
        
        return "Sorry, no joke available right now."
        
    except Exception:
        return "Sorry, I couldn't fetch a joke right now."
