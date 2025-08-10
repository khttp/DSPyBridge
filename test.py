import dspy
from dspy.adapters.types.tool import Tool
import requests

from app.core import config


groq_model = dspy.LM(
                model=config.DEFAULT_MODEL,
                api_key=config.GROQ_API_KEY,
                max_tokens=3000
            )

dspy.configure(lm=groq_model)

def get_joke_tool() -> str:
    """this function returns a random joke"""
    url = "https://sv443.net/jokeapi/v2/joke/Any"
    res = requests.get(url).json()
    if res.get("error") != False:
        return "Sorry, I couldn't fetch a joke."
    return f"{res.get('setup')}\n{res.get('delivery')}"

def get_weather_tool(city: str) -> str:
    """this function takes a city as an input and returns the current weather"""
    api_key = "ce1c42fc470201b40ca2794ef81a3ebd"
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    res = requests.get(url).json()

    if res.get("cod") != 200:
        return "Sorry, I couldn't fetch the weather."

    temp = res["main"]["temp"]
    desc = res["weather"][0]["description"]
    return f"The weather in {city} is {temp}°C with {desc}."


class FinancialAnalysisAgent(dspy.Module):
    """ReAct agent for financial analysis using Yahoo Finance data."""

    def __init__(self):
        super().__init__()

        # Combine all tools
        self.tools = [
            get_weather_tool,
            get_joke_tool
        ]

        # Initialize ReAct
        self.react = dspy.ReAct(
            signature="user_request -> analysis_response",
            tools=self.tools,
            max_iters=6
        )

    def forward(self, user_request: str):
        return self.react(user_request=user_request)
    

def run_financial_demo():
    """Demo of the financial analysis agent."""

    # Initialize agent
    agent = FinancialAnalysisAgent()

    # Example queries
    queries = [
        "tell me a joke",
        "how is it in chicago?",
        "what's the wheather in tala"
    ]

    for query in queries:
        print(f"Query: {query}")
        response = agent(user_request=query)
        print(f"Analysis: {response.analysis_response}")
        print("-" * 50)

# Run the demo
if __name__ == "__main__":
    run_financial_demo()