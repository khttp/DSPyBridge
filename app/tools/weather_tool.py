"""
Simple weather tool for DSPy agents
"""
import requests
from dotenv import load_dotenv
import os

load_dotenv(override=True)

def get_weather_tool(city: str) -> str:
    """
    Get current weather for a city using OpenWeatherMap API.
    
    Args:
        city (str): Name of the city to get weather for
        
    Returns:
        str: Weather information or error message
    """
    api_key = os.getenv("WEATHER_API_KEY")
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
def get_weather_tool(params: dict) -> str:
    """
    Get current weather for a city using OpenWeatherMap API.
    Args:
        params (dict): Should contain 'city' key
    Returns:
        str: Weather information or error message
    """
    city = params.get("city") if params else None
    if not city:
        return "Please provide a city name."
    api_key = os.getenv("WEATHER_API_KEY")
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
