# DSPy Bridge - Simplified Structure

## 🎯 What We Built

A clean, simple FastAPI server with DSPy modules for different AI capabilities.

## 📁 Final Structure

```
DSPyBridge/
├── app/
│   ├── api/              # Individual endpoint modules
│   │   ├── chat.py       # Simple chat (dspy.Predict)
│   │   ├── qa.py         # Q&A + reasoning (dspy.ChainOfThought)
│   │   ├── agent.py      # ReAct agent (dspy.ReAct)
│   │   ├── retrieval.py  # RAG system (dspy.Predict + docs)
│   │   ├── health.py     # Health check
│   │   └── info.py       # API info
│   ├── tools/            # Simple tool functions
│   │   ├── weather_tool.py  # Get weather
│   │   ├── joke_tool.py     # Get jokes
│   │   └── __init__.py      # Tool exports
│   ├── models/
│   │   ├── schemas.py    # Pydantic models
│   │   └── __init__.py
│   ├── core/
│   │   ├── config.py     # Configuration
│   │   ├── logging.py    # Logging setup
│   │   └── __init__.py
│   └── main.py           # FastAPI app
├── docs/                 # Sample documents for RAG
├── tests/               # Test files
└── pyproject.toml       # Dependencies
```

## 🚀 Endpoints

| Endpoint | Module | DSPy Primitive | Use Case |
|----------|--------|----------------|----------|
| `/question` | QuestionModule | dspy.Predict | Simple Q&A |
| `/reasoning` | ReasoningModule | dspy.ChainOfThought | Step-by-step reasoning |
| `/agent` | AgentModule | dspy.ReAct | Tool-based interactions |
| `/rag` | RAGModule | dspy.Predict | Document-based queries |

## 🔧 Key Features

### 1. **Proper DSPy Modules**
Each endpoint uses a proper `dspy.Module` class:

```python
class ChatModule(dspy.Module):
    def __init__(self):
        super().__init__()
        self.predict = dspy.Predict(ChatSignature)
    
    def forward(self, message: str):
        return self.predict(message=message)
```

### 2. **Simple Tools System**
- Weather tool (OpenWeatherMap API)
- Joke tool (JokeAPI)
- Easy to extend with new tools

### 3. **Self-Contained Endpoints**
- Each endpoint manages its own DSPy configuration
- Independent initialization
- Graceful error handling

### 4. **Document RAG**
- Load `.txt` files from `docs/` directory
- Simple keyword-based retrieval
- Document-based Q&A

## 🏃 Quick Start

1. **Set Environment**:
   ```bash
   GROQ_API_KEY=your_groq_api_key
   ```

2. **Install & Run**:
   ```bash
   poetry install
   poetry run uvicorn app.main:app --reload
   ```

3. **Test Endpoints**:
   ```bash
   # Simple Q&A
   curl -X POST http://localhost:8000/question \
     -d '{"question": "What is Python?"}'

   # Agent with tools
   curl -X POST http://localhost:8000/agent \
     -d '{"message": "What is the weather in Paris?"}'

   # Document query
   curl -X POST http://localhost:8000/rag \
     -d '{"query": "What is DSPy?"}'
   ```

## 🎉 Accomplishments

✅ **Clean Architecture**: Each endpoint is a self-contained DSPy module  
✅ **Framework Compliance**: Proper use of `dspy.Module` across all endpoints  
✅ **Tool Integration**: Weather and joke tools working with ReAct agent  
✅ **RAG System**: Document retrieval from txt files  
✅ **Error Handling**: Graceful fallbacks when API keys missing  
✅ **Simplified**: Removed unnecessary complexity, kept it clean  

## 💡 Usage Examples

```python
# Each endpoint demonstrates different DSPy capabilities:

# 1. Simple Q&A with dspy.Predict
POST /question {"question": "What is Python?"}

# 2. Step-by-step reasoning with dspy.ChainOfThought  
POST /reasoning {"question": "Why is the sky blue?"}

# 3. Tool usage with dspy.ReAct
POST /agent {"message": "Tell me a joke about weather in London"}

# 4. Document retrieval with dspy.Predict + context
POST /rag {"query": "What is DSPy?", "top_k": 3}
```

## 🔮 Ready for Production

The simplified structure is now:
- **Easy to understand** - Clear separation of concerns
- **Easy to extend** - Add new endpoints or tools
- **Easy to test** - Each module can be tested independently
- **Production ready** - Proper error handling and configuration

Perfect for building intelligent chatbots and AI applications with DSPy! 🎯
