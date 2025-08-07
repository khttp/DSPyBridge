"""
Example client for the DSPy FastAPI Server.

This script demonstrates how to interact with all the available endpoints.
"""

import requests
import json
from typing import Dict, Any, List
import time

class DSPyClient:
    """Client for interacting with the DSPy FastAPI Server."""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
    
    def health_check(self) -> Dict[str, Any]:
        """Check server health."""
        response = self.session.get(f"{self.base_url}/health")
        response.raise_for_status()
        return response.json()
    
    def list_modules(self) -> Dict[str, Any]:
        """List available modules."""
        response = self.session.get(f"{self.base_url}/modules")
        response.raise_for_status()
        return response.json()
    
    def completion(self, prompt: str, max_tokens: int = 100, temperature: float = 0.7) -> Dict[str, Any]:
        """Generate text completion."""
        data = {
            "prompt": prompt,
            "max_tokens": max_tokens,
            "temperature": temperature
        }
        response = self.session.post(f"{self.base_url}/completion", json=data)
        response.raise_for_status()
        return response.json()
    
    def chain_of_thought(self, question: str, context: str = None) -> Dict[str, Any]:
        """Perform chain of thought reasoning."""
        data = {"question": question}
        if context:
            data["context"] = context
        response = self.session.post(f"{self.base_url}/chain-of-thought", json=data)
        response.raise_for_status()
        return response.json()
    
    def few_shot_learning(self, examples: List[Dict[str, str]], new_input: str, task_description: str) -> Dict[str, Any]:
        """Perform few-shot learning."""
        data = {
            "examples": examples,
            "new_input": new_input,
            "task_description": task_description
        }
        response = self.session.post(f"{self.base_url}/few-shot", json=data)
        response.raise_for_status()
        return response.json()
    
    def retrieval_qa(self, query: str, documents: List[str], top_k: int = 3) -> Dict[str, Any]:
        """Perform retrieval-augmented generation."""
        data = {
            "query": query,
            "documents": documents,
            "top_k": top_k
        }
        response = self.session.post(f"{self.base_url}/retrieval", json=data)
        response.raise_for_status()
        return response.json()
    
    def optimize_module(self, module_type: str, training_data: List[Dict[str, Any]], metric: str = "accuracy") -> Dict[str, Any]:
        """Optimize a DSPy module."""
        data = {
            "module_type": module_type,
            "training_data": training_data,
            "metric": metric
        }
        response = self.session.post(f"{self.base_url}/optimize", json=data)
        response.raise_for_status()
        return response.json()
    
    def evaluate_module(self, module_config: Dict[str, Any], test_data: List[Dict[str, Any]], metrics: List[str] = None) -> Dict[str, Any]:
        """Evaluate a DSPy module."""
        if metrics is None:
            metrics = ["accuracy"]
        data = {
            "module_config": module_config,
            "test_data": test_data,
            "metrics": metrics
        }
        response = self.session.post(f"{self.base_url}/evaluate", json=data)
        response.raise_for_status()
        return response.json()

def run_examples():
    """Run example interactions with the DSPy server."""
    client = DSPyClient()
    
    print("🚀 DSPy FastAPI Server Client Examples\n")
    
    # Health check
    print("1. Health Check")
    try:
        health = client.health_check()
        print(f"✅ Server is healthy: {health['status']}")
        print(f"   Version: {health['version']}")
        print(f"   DSPy Version: {health['dspy_version']}\n")
    except Exception as e:
        print(f"❌ Health check failed: {e}\n")
        return
    
    # List modules
    print("2. Available Modules")
    try:
        modules = client.list_modules()
        print("✅ Available modules:")
        for name, info in modules["available_modules"].items():
            print(f"   • {name}: {info['description']}")
        print()
    except Exception as e:
        print(f"❌ Failed to list modules: {e}\n")
    
    # Basic completion
    print("3. Basic Text Completion")
    try:
        result = client.completion(
            prompt="What is the capital of France?",
            max_tokens=50,
            temperature=0.7
        )
        print(f"✅ Completion: {result['completion'][:100]}...")
        print()
    except Exception as e:
        print(f"❌ Completion failed: {e}\n")
    
    # Chain of thought
    print("4. Chain of Thought Reasoning")
    try:
        result = client.chain_of_thought(
            question="If a train travels 60 mph for 2 hours, how far does it go?",
            context="This is a basic physics problem about distance, speed, and time."
        )
        print(f"✅ Question: {result['question']}")
        print(f"   Reasoning: {result['reasoning'][:100]}...")
        print(f"   Answer: {result['answer']}")
        print()
    except Exception as e:
        print(f"❌ Chain of thought failed: {e}\n")
    
    # Few-shot learning
    print("5. Few-Shot Learning")
    try:
        examples = [
            {"input": "This movie was amazing!", "output": "positive"},
            {"input": "I hated this film.", "output": "negative"},
            {"input": "The movie was okay.", "output": "neutral"}
        ]
        result = client.few_shot_learning(
            examples=examples,
            new_input="This film was absolutely fantastic!",
            task_description="Classify the sentiment of movie reviews as positive, negative, or neutral."
        )
        print(f"✅ Input: {result['input']}")
        print(f"   Output: {result['output']}")
        print(f"   Examples used: {result['examples_used']}")
        print()
    except Exception as e:
        print(f"❌ Few-shot learning failed: {e}\n")
    
    # Retrieval-augmented generation
    print("6. Retrieval-Augmented Generation")
    try:
        documents = [
            "Paris is the capital and largest city of France. It is located in the north of the country.",
            "London is the capital of England and the United Kingdom. It is situated on the River Thames.",
            "Tokyo is the capital of Japan and one of the most populous cities in the world.",
            "Berlin is the capital and largest city of Germany. It is located in northeastern Germany.",
            "Rome is the capital city of Italy and was the center of the Roman Empire."
        ]
        result = client.retrieval_qa(
            query="What is the capital of France?",
            documents=documents,
            top_k=2
        )
        print(f"✅ Query: {result['query']}")
        print(f"   Retrieved docs: {len(result['retrieved_docs'])}")
        print(f"   Response: {result['generated_response']}")
        print()
    except Exception as e:
        print(f"❌ Retrieval-augmented generation failed: {e}\n")
    
    # Module optimization
    print("7. Module Optimization")
    try:
        training_data = [
            {"input": "What is 2+2?", "output": "4"},
            {"input": "What is the capital of Italy?", "output": "Rome"},
            {"input": "Who wrote Romeo and Juliet?", "output": "Shakespeare"}
        ]
        result = client.optimize_module(
            module_type="basic_qa",
            training_data=training_data,
            metric="accuracy"
        )
        print(f"✅ Optimization completed for: {result['module_type']}")
        print(f"   Best score: {result['performance_metrics']['accuracy']}")
        print()
    except Exception as e:
        print(f"❌ Module optimization failed: {e}\n")
    
    # Module evaluation
    print("8. Module Evaluation")
    try:
        test_data = [
            {"input": "What is 3+3?", "output": "6"},
            {"input": "What is the capital of Spain?", "output": "Madrid"}
        ]
        result = client.evaluate_module(
            module_config={"type": "basic_qa", "temperature": 0.7},
            test_data=test_data,
            metrics=["accuracy", "precision"]
        )
        print(f"✅ Evaluation completed")
        print(f"   Results: {result['results']}")
        print(f"   Predictions: {len(result['predictions'])} items")
        print()
    except Exception as e:
        print(f"❌ Module evaluation failed: {e}\n")
    
    print("🎉 All examples completed!")

if __name__ == "__main__":
    print("Starting DSPy Client Examples...")
    print("Make sure the DSPy FastAPI server is running on http://localhost:8000\n")
    
    # Wait for user confirmation
    input("Press Enter to continue with examples (or Ctrl+C to exit)...")
    
    run_examples()
