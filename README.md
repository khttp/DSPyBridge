# DSPy FastAPI Server

A FastAPI server that uses DSPy framework with Groq for AI-powered chat and question answering capabilities.

## Features

- **Chat API**: Main endpoint for chatbot integration using DSPy
- **Question Answering**: Direct Q&A with optional context
- **Chain of Thought Reasoning**: Detailed reasoning with step-by-step explanations
- **Groq Integration**: Fast inference using Groq's language models
- **Health Monitoring**: Check server and DSPy configuration status
- **Module Optimization**: Optimize DSPy modules using training data
- **Module Evaluation**: Evaluate module performance on test data
- **Health Monitoring**: Server health and status endpoints
- **Comprehensive Documentation**: OpenAPI/Swagger documentation
- **Error Handling**: Robust error handling and logging
- **CORS Support**: Cross-origin resource sharing enabled

## 📋 Requirements

- Python 3.11+
- Poetry (for dependency management)
- DSPy-AI
- FastAPI
- Uvicorn

## 🛠️ Installation

1. **Clone the repository** (or ensure you have the project files):
```bash
cd dspyProject
```

2. **Install dependencies**:
```bash
poetry install
```

3. **Set up environment variables** (optional):
```bash
# Create a .env file
cp .env.example .env

# Edit .env with your API keys
OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here
```

## 🚀 Running the Server

### Development Mode
```bash
poetry run python main.py
```

### Production Mode
```bash
poetry run uvicorn main:app --host 0.0.0.0 --port 8000
```

The server will start on `http://localhost:8000`

## 📚 API Documentation

Once the server is running, you can access:

- **Interactive API Documentation**: http://localhost:8000/docs
- **ReDoc Documentation**: http://localhost:8000/redoc
- **OpenAPI Schema**: http://localhost:8000/openapi.json

## 🔧 API Endpoints

### Health Check
```
GET /health
```
Check server health and get version information.

### List Modules
```
GET /modules
```
List all available DSPy modules and their capabilities.

### Text Completion
```
POST /completion
```
Generate text completions using DSPy.

**Request Body:**
```json
{
  "prompt": "What is the capital of France?",
  "max_tokens": 100,
  "temperature": 0.7
}
```

### Chain of Thought
```
POST /chain-of-thought
```
Perform step-by-step reasoning.

**Request Body:**
```json
{
  "question": "If a train travels 60 mph for 2 hours, how far does it go?",
  "context": "This is a basic physics problem."
}
```

### Few-Shot Learning
```
POST /few-shot
```
Learn from examples and apply to new inputs.

**Request Body:**
```json
{
  "examples": [
    {"input": "This movie was amazing!", "output": "positive"},
    {"input": "I hated this film.", "output": "negative"}
  ],
  "new_input": "This film was fantastic!",
  "task_description": "Classify sentiment as positive or negative"
}
```

### Retrieval-Augmented Generation
```
POST /retrieval
```
Combine document retrieval with text generation.

**Request Body:**
```json
{
  "query": "What is the capital of France?",
  "documents": [
    "Paris is the capital of France...",
    "London is the capital of England..."
  ],
  "top_k": 3
}
```

### Module Optimization
```
POST /optimize
```
Optimize DSPy modules using training data.

**Request Body:**
```json
{
  "module_type": "basic_qa",
  "training_data": [
    {"input": "What is 2+2?", "output": "4"}
  ],
  "metric": "accuracy"
}
```

### Module Evaluation
```
POST /evaluate
```
Evaluate module performance on test data.

**Request Body:**
```json
{
  "module_config": {"type": "basic_qa"},
  "test_data": [
    {"input": "What is 3+3?", "output": "6"}
  ],
  "metrics": ["accuracy", "precision"]
}
```

## 🧪 Example Usage

### Using the Python Client

```python
from client_example import DSPyClient

# Initialize client
client = DSPyClient("http://localhost:8000")

# Check health
health = client.health_check()
print(f"Server status: {health['status']}")

# Basic completion
result = client.completion("What is the meaning of life?")
print(f"Answer: {result['completion']}")

# Chain of thought reasoning
result = client.chain_of_thought("How do you solve 2x + 5 = 15?")
print(f"Reasoning: {result['reasoning']}")
print(f"Answer: {result['answer']}")
```

### Using cURL

```bash
# Health check
curl -X GET "http://localhost:8000/health"

# Text completion
curl -X POST "http://localhost:8000/completion" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "What is artificial intelligence?",
    "max_tokens": 150,
    "temperature": 0.7
  }'

# Chain of thought
curl -X POST "http://localhost:8000/chain-of-thought" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "Why is the sky blue?",
    "context": "This is a question about physics and light scattering."
  }'
```

## 🔧 Configuration

The server can be configured using environment variables or the `config.py` file:

### Environment Variables

```bash
# Server settings
APP_NAME="DSPy API Server"
DEBUG=false
HOST="0.0.0.0"
PORT=8000

# Model settings
DEFAULT_MODEL="openai/gpt-3.5-turbo"
OPENAI_API_KEY="your-api-key"
DEFAULT_TEMPERATURE=0.7
DEFAULT_MAX_TOKENS=150

# Optimization settings
OPTIMIZATION_TRIALS=20
OPTIMIZATION_TIMEOUT=300

# Logging
LOG_LEVEL="INFO"
```

### Model Configuration

The server supports multiple language model providers:

- **OpenAI**: GPT-3.5, GPT-4, GPT-4 Turbo
- **Anthropic**: Claude-3, Claude-3 Haiku
- **Local Models**: Ollama, Hugging Face Transformers

## 🧪 Running Examples

The project includes a comprehensive example client:

```bash
# Run the example client
poetry run python client_example.py
```

This will demonstrate all available endpoints and their usage.

## 🔧 Development

### Project Structure

```
dspyProject/
├── main.py              # Main FastAPI application
├── config.py            # Configuration settings
├── client_example.py    # Example client
├── pyproject.toml       # Poetry configuration
├── poetry.lock          # Locked dependencies
└── README.md           # This file
```

### Adding New Endpoints

1. Define Pydantic models for request/response
2. Create DSPy signatures and modules
3. Implement endpoint handler
4. Add to client example
5. Update documentation

### Running Tests

```bash
# Install development dependencies
poetry install --dev

# Run tests
poetry run pytest

# Run with coverage
poetry run pytest --cov=.
```

## 🐛 Troubleshooting

### Common Issues

1. **DSPy Configuration Errors**:
   - Ensure API keys are properly set
   - Check model availability and quotas
   - Verify network connectivity

2. **Dependency Issues**:
   - Update Poetry: `poetry self update`
   - Clear cache: `poetry cache clear --all .`
   - Reinstall: `poetry install --no-cache`

3. **Port Already in Use**:
   ```bash
   # Find and kill process using port 8000
   lsof -ti:8000 | xargs kill -9
   ```

### Logging

The server provides comprehensive logging. Set log level in configuration:

```python
LOG_LEVEL = "DEBUG"  # DEBUG, INFO, WARNING, ERROR
```

Logs include:
- Request/response details
- DSPy module operations
- Error traces
- Performance metrics

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Update documentation
6. Submit a pull request

## 📄 License

This project is licensed under the MIT License. See LICENSE file for details.

## 🙏 Acknowledgments

- [DSPy](https://github.com/stanfordnlp/dspy) - The underlying AI programming framework
- [FastAPI](https://fastapi.tiangolo.com/) - The web framework
- [Poetry](https://python-poetry.org/) - Dependency management

## 📞 Support

For questions and support:
- Check the [DSPy documentation](https://dspy-docs.vercel.app/)
- Review the API documentation at `/docs`
- Open an issue for bugs or feature requests

---

**Happy coding with DSPy! 🎉**
