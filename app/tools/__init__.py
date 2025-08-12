"""
Simple tools for DSPy agents
"""
from .weather_tool import get_weather_tool
from .joke_tool import get_joke_tool
from .time_tool import get_current_time_tool, get_current_date_tool

def get_default_tools():
    """Get the default set of tools (as callables)"""
    return [
        get_weather_tool,
        get_joke_tool,
        get_current_time_tool,
        get_current_date_tool
    ]

__all__ = [
    "get_weather_tool",
    "get_joke_tool",
    "get_current_time_tool",
    "get_current_date_tool",
    "get_default_tools"
]
