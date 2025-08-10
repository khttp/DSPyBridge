"""
Simple tools for DSPy agents
"""
from .weather_tool import get_weather_tool
from .joke_tool import get_joke_tool

def get_default_tools():
    """Get the default set of tools"""
    return [get_weather_tool, get_joke_tool]

__all__ = [
    "get_weather_tool",
    "get_joke_tool", 
    "get_default_tools"
]
