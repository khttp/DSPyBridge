# DSPy Tools Documentation

## Overview

The `app/tools/` directory contains all tool functions used by DSPy ReAct agents. Tools are organized by functionality and can be easily managed through the tool registry system.

## Tool Structure

```
app/tools/
├── __init__.py           # Module exports
├── tool_manager.py       # Tool registry and management
├── weather_tool.py       # Weather-related tools
├── joke_tool.py          # Entertainment tools
└── time_tool.py          # Time and date tools
```

## Available Tools

### Weather Tools (`weather_tool.py`)

#### `get_weather_tool(city: str) -> str`
Get current weather information for a city using OpenWeatherMap API.

**Example:**
```python
result = get_weather_tool("Paris")
# Returns: "The weather in Paris is 15°C with clear sky. Feels like 14°C, humidity 65%."
```

### Entertainment Tools (`joke_tool.py`)

#### `get_joke_tool() -> str`
Get a random joke from JokeAPI.

**Example:**
```python
result = get_joke_tool()
# Returns: "Why don't scientists trust atoms?\nBecause they make up everything!"
```

#### `get_dad_joke_tool() -> str`
Get a random dad joke from icanhazdadjoke API.

**Example:**
```python
result = get_dad_joke_tool()
# Returns: "Dad joke: I invented a new word: Plagiarism!"
```

### Time Tools (`time_tool.py`)

#### `get_current_time_tool(timezone_name: str = "UTC") -> str`
Get current time for a specific timezone.

**Example:**
```python
result = get_current_time_tool("US/Eastern")
# Returns: "Current time in US/Eastern: 2025-08-10 14:30:45 EDT"
```

#### `get_current_date_tool() -> str`
Get current date.

**Example:**
```python
result = get_current_date_tool()
# Returns: "Today is Saturday, 2025-08-10"
```

## Tool Management

### ToolRegistry Class

The `ToolRegistry` class provides a centralized way to manage all available tools.

```python
from app.tools import tool_registry

# List all available tools
tools = tool_registry.list_tool_names()
# Returns: ['weather', 'joke', 'dad_joke', 'time', 'date']

# Get tool information
info = tool_registry.get_tool_info()
# Returns: {'weather': 'Get current weather for a city...', ...}

# Get specific tools
weather_tool = tool_registry.get_tool('weather')
```

### Predefined Tool Sets

#### `get_default_tools() -> List[Callable]`
Returns the standard set of tools for most agents:
- Weather tool
- Joke tool

#### `get_extended_tools() -> List[Callable]`
Returns an extended set including:
- Weather tool
- Joke tool
- Dad joke tool

#### `get_tools_by_category(category: str) -> List[Callable]`
Get tools by category:
- `"entertainment"`: Joke tools
- `"weather"`: Weather tools
- `"utility"`: Weather, time, and date tools
- `"time"`: Time and date tools

## Usage in Agents

### Basic Usage

```python
from app.tools import get_default_tools

tools = get_default_tools()
agent = dspy.ReAct(
    signature="user_request -> analysis_response",
    tools=tools,
    max_iters=6
)
```

### Category-based Usage

```python
from app.tools import get_tools_by_category

# Entertainment-focused agent
entertainment_tools = get_tools_by_category("entertainment")

# Utility-focused agent
utility_tools = get_tools_by_category("utility")
```

### Custom Tool Selection

```python
from app.tools import tool_registry

# Select specific tools
selected_tools = tool_registry.get_tools_by_names(["weather", "time"])
```

## Adding New Tools

### 1. Create Tool Function

Create a new file in `app/tools/` with your tool functions:

```python
# app/tools/calculator_tool.py
def add_numbers_tool(a: float, b: float) -> str:
    """Add two numbers together"""
    try:
        result = a + b
        return f"{a} + {b} = {result}"
    except Exception as e:
        return f"Error in calculation: {str(e)}"
```

### 2. Register Tool

Add your tool to the registry in `tool_manager.py`:

```python
from .calculator_tool import add_numbers_tool

def _register_default_tools(self):
    # ... existing tools ...
    self.register("calculator", add_numbers_tool)
```

### 3. Update Exports

Add to `__init__.py`:

```python
from .calculator_tool import add_numbers_tool

__all__ = [
    # ... existing exports ...
    "add_numbers_tool",
]
```

## Error Handling

All tools implement consistent error handling:

1. **Network Errors**: Graceful handling of API timeouts and failures
2. **Input Validation**: Proper validation of parameters
3. **Fallback Responses**: Meaningful error messages for users
4. **Exception Safety**: Tools never crash the agent

Example error handling pattern:

```python
def example_tool(param: str) -> str:
    try:
        # Tool implementation
        result = some_api_call(param)
        return f"Success: {result}"
    except requests.RequestException as e:
        return f"Network error: {str(e)}"
    except ValueError as e:
        return f"Invalid input: {str(e)}"
    except Exception as e:
        return f"Error: {str(e)}"
```

## Tool Testing

Each tool can be tested independently:

```python
# Test weather tool
from app.tools import get_weather_tool
result = get_weather_tool("London")
assert "London" in result

# Test joke tool
from app.tools import get_joke_tool
result = get_joke_tool()
assert len(result) > 0
```

## Best Practices

1. **Clear Docstrings**: Each tool should have descriptive documentation
2. **Type Hints**: Use proper type annotations
3. **Error Handling**: Always handle exceptions gracefully
4. **Timeouts**: Use timeouts for network requests
5. **Validation**: Validate inputs before processing
6. **Consistency**: Follow the established pattern for tool functions
7. **Testing**: Test tools independently before integration

## API Dependencies

Some tools require external APIs:

- **Weather Tool**: OpenWeatherMap API (free tier available)
- **Joke Tools**: Public APIs (no authentication required)
- **Time Tools**: No external dependencies

## Future Enhancements

Potential tools to add:

1. **Web Search**: Search the internet
2. **File Operations**: Read/write files
3. **Database Queries**: Query databases
4. **Email**: Send emails
5. **Calendar**: Manage calendar events
6. **Translation**: Translate text
7. **Image Generation**: Generate images
8. **News**: Get news headlines

## Integration with DSPy

Tools are fully compatible with DSPy's ReAct module:

```python
import dspy
from app.tools import get_default_tools

class MyAgent(dspy.Module):
    def __init__(self):
        super().__init__()
        tools = get_default_tools()
        self.react = dspy.ReAct(
            signature="user_request -> analysis_response",
            tools=tools,
            max_iters=6
        )
    
    def forward(self, user_request: str):
        return self.react(user_request=user_request)
```

This modular approach makes it easy to extend functionality and maintain clean separation of concerns in your DSPy-powered applications.
