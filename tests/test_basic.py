"""
Basic unit tests for DSPyBridge
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import pytest
import asyncio
from app.tools import get_joke_from_api, is_joke_request


class TestJokeAPI:
    """Test the joke API functionality"""
    
    @pytest.mark.asyncio
    async def test_get_joke_success(self):
        """Test that joke API returns valid joke"""
        result = await get_joke_from_api()
        
        assert result["success"] is True
        assert "joke" in result
        assert "setup" in result["joke"]
        assert "punchline" in result["joke"]
        assert "type" in result["joke"]
    
    def test_is_joke_request_positive(self):
        """Test joke request detection with positive cases"""
        test_cases = [
            "Tell me a joke",
            "I want something funny",
            "Make me laugh",
            "Got any humor?",
            "Give me a comedy"
        ]
        
        for message in test_cases:
            assert is_joke_request(message) is True
    
    def test_is_joke_request_negative(self):
        """Test joke request detection with negative cases"""
        test_cases = [
            "What is the capital of France?",
            "How does DSPy work?",
            "Tell me about AI",
            "What's the weather like?",
            "Hello there"
        ]
        
        for message in test_cases:
            assert is_joke_request(message) is False


if __name__ == "__main__":
    # Simple test runner for basic testing
    async def run_tests():
        test_instance = TestJokeAPI()
        
        print("🧪 Running DSPyBridge Tests")
        print("=" * 30)
        
        # Test joke API
        print("Testing joke API...")
        try:
            await test_instance.test_get_joke_success()
            print("✅ Joke API test passed")
        except Exception as e:
            print(f"❌ Joke API test failed: {e}")
        
        # Test joke detection
        print("Testing joke detection...")
        try:
            test_instance.test_is_joke_request_positive()
            test_instance.test_is_joke_request_negative()
            print("✅ Joke detection tests passed")
        except Exception as e:
            print(f"❌ Joke detection tests failed: {e}")
        
        print("\n🎉 Basic tests completed!")
    
    asyncio.run(run_tests())
