"""
Time and date tools for DSPy agents
"""
from datetime import datetime, timezone
from typing import Dict, Any

try:
    import pytz
    PYTZ_AVAILABLE = True
except ImportError:
    PYTZ_AVAILABLE = False


def get_current_time_tool(params: Dict[str, Any] = None) -> str:
    """
    Get current time for a specific timezone.
    
    Args:
        params (Dict[str, Any]): Parameters containing:
            timezone_name (str): Timezone name (e.g., 'UTC', 'US/Eastern', 'Europe/London')
        
    Returns:
        str: Current time in the specified timezone or error message
    """
    # Extract timezone from params or use default
    timezone_name = params.get("timezone_name", "UTC") if params else "UTC"
    try:
        if timezone_name.upper() == "UTC":
            tz = timezone.utc
            current_time = datetime.now(tz)
        elif PYTZ_AVAILABLE:
            tz = pytz.timezone(timezone_name)
            current_time = datetime.now(tz)
        else:
            # Fallback to UTC if pytz not available
            current_time = datetime.now(timezone.utc)
            timezone_name = "UTC (pytz not available)"
        
        formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S %Z")
        
        return f"Current time in {timezone_name}: {formatted_time}"
        
    except Exception as e:
        if PYTZ_AVAILABLE and "UnknownTimeZoneError" in str(type(e)):
            return f"Unknown timezone: {timezone_name}. Try 'UTC', 'US/Eastern', 'Europe/London', etc."
        return f"Error getting time: {str(e)}"


def get_current_date_tool() -> str:
    """
    Get current date.
    
    Returns:
        str: Current date in ISO format
    """
    try:
        current_date = datetime.now().strftime("%Y-%m-%d")
        day_name = datetime.now().strftime("%A")
        
        return f"Today is {day_name}, {current_date}"
        
    except Exception as e:
        return f"Error getting date: {str(e)}"
