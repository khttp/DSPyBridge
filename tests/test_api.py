"""
API integration tests for DSPyBridge
"""
import requests
import json
from typing import Dict, Any


BASE_URL = "http://localhost:8000"


def test_api_endpoint(endpoint: str, method: str = "GET", data: Dict[str, Any] = None) -> Dict[str, Any]:
    """Test an API endpoint and return the result"""
    try:
        if method == "GET":
            response = requests.get(f"{BASE_URL}{endpoint}")
        else:
            response = requests.post(f"{BASE_URL}{endpoint}", json=data)
        
        return {
            "success": response.status_code == 200,
            "status_code": response.status_code,
            "data": response.json() if response.status_code == 200 else None,
            "error": response.text if response.status_code != 200 else None
        }
    except Exception as e:
        return {
            "success": False,
            "status_code": 0,
            "data": None,
            "error": str(e)
        }


def main():
    """Run API integration tests"""
    print("🧪 DSPyBridge API Integration Tests")
    print("=" * 40)
    
    tests = [
        {
            "name": "Health Check",
            "endpoint": "/health",
            "method": "GET"
        },
        {
            "name": "ReAct Joke Request",
            "endpoint": "/react",
            "method": "POST",
            "data": {"message": "Tell me a funny joke!", "enable_tools": True}
        },
        {
            "name": "ReAct Normal Chat",
            "endpoint": "/react", 
            "method": "POST",
            "data": {"message": "What is 2+2?", "enable_tools": True}
        },
        {
            "name": "Basic Chat",
            "endpoint": "/chat",
            "method": "POST", 
            "data": {"message": "Hello there!"}
        },
        {
            "name": "Question Answering",
            "endpoint": "/question",
            "method": "POST",
            "data": {"question": "What is the capital of France?"}
        },
        {
            "name": "Chain of Thought",
            "endpoint": "/reasoning",
            "method": "POST",
            "data": {"question": "If 2+2=4, what is 4+4?"}
        },
        {
            "name": "Endpoints Info",
            "endpoint": "/endpoints",
            "method": "GET"
        }
    ]
    
    results = []
    for test in tests:
        print(f"\n🔄 Testing: {test['name']}")
        
        result = test_api_endpoint(
            test["endpoint"], 
            test.get("method", "GET"),
            test.get("data")
        )
        
        if result["success"]:
            print(f"✅ {test['name']}: PASSED")
            if "response" in result.get("data", {}):
                # Truncate long responses
                response_text = result["data"]["response"]
                if len(response_text) > 100:
                    response_text = response_text[:100] + "..."
                print(f"   Response: {response_text}")
        else:
            print(f"❌ {test['name']}: FAILED")
            print(f"   Error: {result['error']}")
        
        results.append({"test": test["name"], "success": result["success"]})
    
    # Summary
    print("\n📊 Test Results Summary:")
    print("-" * 25)
    passed = sum(1 for r in results if r["success"])
    total = len(results)
    
    for result in results:
        status = "✅ PASS" if result["success"] else "❌ FAIL"
        print(f"  {status}: {result['test']}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! DSPyBridge is working correctly.")
    else:
        print("⚠️  Some tests failed. Check server status and configuration.")
        print("💡 Tip: Make sure the server is running with 'uvicorn app.main:app --reload'")


if __name__ == "__main__":
    main()
