"""
Simple weather tool for DSPy agents
"""
import requests


def get_weather_tool(city: str) -> str:
    """
    Get current weather for a city using OpenWeatherMap API.
    
    Args:
        city (str): Name of the city to get weather for
        
    Returns:
        str: Weather information or error message
    """
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        
        response = requests.get(url, timeout=15)
        data = response.json()
        
        if data.get("cod") != 200:
            return f"Sorry, I couldn't fetch the weather for {city}."
        
        temp = data["main"]["temp"]
        description = data["weather"][0]["description"]
        
        return f"The weather in {city} is {temp}°C with {description}."
        
    except Exception:
        return f"Sorry, I couldn't fetch the weather for {city}."
