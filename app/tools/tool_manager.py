"""
Tool management utilities for DSPy agents
"""
from typing import List, Callable, Dict, Any
from .weather_tool import get_weather_tool
from .joke_tool import get_joke_tool, get_dad_joke_tool
from .time_tool import get_current_time_tool, get_current_date_tool


class ToolRegistry:
    """Registry for managing available tools"""
    
    def __init__(self):
        self._tools: Dict[str, Callable] = {}
        self._register_default_tools()
    
    def _register_default_tools(self):
        """Register default tools"""
        self.register("weather", get_weather_tool)
        self.register("joke", get_joke_tool)
        self.register("dad_joke", get_dad_joke_tool)
        self.register("time", get_current_time_tool)
        self.register("date", get_current_date_tool)
    
    def register(self, name: str, tool_func: Callable):
        """Register a new tool"""
        self._tools[name] = tool_func
    
    def get_tool(self, name: str) -> Callable:
        """Get a tool by name"""
        return self._tools.get(name)
    
    def get_all_tools(self) -> List[Callable]:
        """Get all registered tools"""
        return list(self._tools.values())
    
    def get_tools_by_names(self, names: List[str]) -> List[Callable]:
        """Get specific tools by names"""
        return [self._tools[name] for name in names if name in self._tools]
    
    def list_tool_names(self) -> List[str]:
        """List all available tool names"""
        return list(self._tools.keys())
    
    def get_tool_info(self) -> Dict[str, str]:
        """Get information about all tools"""
        info = {}
        for name, tool in self._tools.items():
            doc = tool.__doc__ or "No description available"
            info[name] = doc.strip().split('\n')[0]  # First line of docstring
        return info


# Global tool registry instance
tool_registry = ToolRegistry()


def get_default_tools() -> List[Callable]:
    """Get the default set of tools for agents"""
    return [get_weather_tool, get_joke_tool]


def get_extended_tools() -> List[Callable]:
    """Get an extended set of tools including dad jokes"""
    return [get_weather_tool, get_joke_tool, get_dad_joke_tool]


def get_tools_by_category(category: str) -> List[Callable]:
    """Get tools by category"""
    categories = {
        "entertainment": [get_joke_tool, get_dad_joke_tool],
        "weather": [get_weather_tool],
        "utility": [get_weather_tool, get_current_time_tool, get_current_date_tool],
        "fun": [get_joke_tool, get_dad_joke_tool],
        "time": [get_current_time_tool, get_current_date_tool]
    }
    return categories.get(category, [])
