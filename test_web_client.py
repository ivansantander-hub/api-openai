#!/usr/bin/env python3
"""
Test script to verify all API endpoints work correctly
This is useful for testing the backend before using the web client
"""

import requests
import json
import time

API_BASE_URL = "http://localhost:8000"

def test_health():
    """Test the health endpoint"""
    print("🏥 Testing Health Check...")
    try:
        response = requests.get(f"{API_BASE_URL}/health")
        data = response.json()
        print(f"✅ Status: {data['status']}")
        print(f"📡 Message: {data['message']}")
        print(f"🤖 OpenAI Client: {data['openai_client']}")
        return True
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False

def test_models():
    """Test the models endpoint"""
    print("\n📋 Testing List Models...")
    try:
        response = requests.get(f"{API_BASE_URL}/models")
        data = response.json()
        print(f"✅ Found {data['count']} models")
        # Show first 5 models
        for i, model in enumerate(data['models'][:5]):
            print(f"   {i+1}. {model['id']}")
        if data['count'] > 5:
            print(f"   ... and {data['count'] - 5} more models")
        return True
    except Exception as e:
        print(f"❌ Models test failed: {e}")
        return False

def test_chat():
    """Test the chat endpoint"""
    print("\n💬 Testing Chat Completion...")
    try:
        payload = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {"role": "user", "content": "Say hello in exactly 5 words"}
            ],
            "temperature": 0.7,
            "max_tokens": 50
        }
        response = requests.post(f"{API_BASE_URL}/chat", json=payload)
        data = response.json()
        print(f"✅ Response: {data['message']}")
        print(f"📊 Tokens used: {data['usage']['total_tokens'] if data.get('usage') else 'N/A'}")
        return True
    except Exception as e:
        print(f"❌ Chat test failed: {e}")
        return False

def test_completion():
    """Test the completion endpoint"""
    print("\n📝 Testing Text Completion...")
    try:
        payload = {
            "model": "gpt-3.5-turbo-instruct",
            "prompt": "The capital of France is",
            "temperature": 0.3,
            "max_tokens": 20
        }
        response = requests.post(f"{API_BASE_URL}/completion", json=payload)
        data = response.json()
        print(f"✅ Completion: {data['text'].strip()}")
        print(f"📊 Tokens used: {data['usage']['total_tokens'] if data.get('usage') else 'N/A'}")
        return True
    except Exception as e:
        print(f"❌ Completion test failed: {e}")
        return False

def test_embeddings():
    """Test the embeddings endpoint"""
    print("\n🔢 Testing Embeddings...")
    try:
        payload = {
            "model": "text-embedding-ada-002",
            "input": "Hello world"
        }
        response = requests.post(f"{API_BASE_URL}/embeddings", json=payload)
        data = response.json()
        embedding_length = len(data['embeddings'][0])
        print(f"✅ Generated embedding with {embedding_length} dimensions")
        print(f"📊 First 5 values: {data['embeddings'][0][:5]}")
        return True
    except Exception as e:
        print(f"❌ Embeddings test failed: {e}")
        return False

def test_images():
    """Test the image generation endpoint"""
    print("\n🎨 Testing Image Generation...")
    try:
        payload = {
            "prompt": "A cute cat wearing a hat",
            "size": "1024x1024",
            "quality": "standard",
            "n": 1
        }
        response = requests.post(f"{API_BASE_URL}/images/generate", json=payload)
        data = response.json()
        print(f"✅ Generated image: {data['url'][:50]}...")
        print(f"🎯 Revised prompt: {data['revised_prompt'][:50]}...")
        return True
    except Exception as e:
        print(f"❌ Image generation test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Testing OpenAI API Service Endpoints")
    print("=" * 50)
    
    tests = [
        ("Health Check", test_health),
        ("List Models", test_models),
        ("Chat Completion", test_chat),
        ("Text Completion", test_completion),
        ("Embeddings", test_embeddings),
        ("Image Generation", test_images),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n🧪 Running: {test_name}")
        print("-" * 30)
        
        start_time = time.time()
        success = test_func()
        duration = time.time() - start_time
        
        results.append({
            "name": test_name,
            "success": success,
            "duration": duration
        })
        
        print(f"⏱️  Duration: {duration:.2f}s")
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 TEST SUMMARY")
    print("=" * 50)
    
    passed = sum(1 for r in results if r["success"])
    total = len(results)
    
    for result in results:
        status = "✅ PASS" if result["success"] else "❌ FAIL"
        print(f"{status} {result['name']:<20} ({result['duration']:.2f}s)")
    
    print(f"\nResults: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Your API is working perfectly!")
        print("🌐 Open http://localhost:8000 to use the web client")
    else:
        print("⚠️  Some tests failed. Check your OpenAI API key configuration.")
        print("💡 Make sure you have a .env file with OPENAI_API_KEY=your_key")

if __name__ == "__main__":
    main() 