#!/usr/bin/env python3
"""
Test script for the modular backend architecture.
This script tests all API endpoints to ensure they work correctly.
"""

import requests
import json
import time
from typing import Optional

# Configuration
BASE_URL = "http://localhost:8000"
ACCESS_KEY = "your-test-key"  # Replace with actual access key for testing

class BackendTester:
    """Test class for the modular backend."""
    
    def __init__(self, base_url: str, access_key: Optional[str] = None):
        self.base_url = base_url
        self.access_key = access_key
        self.token = None
        
    def test_health(self):
        """Test health endpoint."""
        print("🔍 Testing health endpoint...")
        try:
            response = requests.get(f"{self.base_url}/health")
            print(f"Status: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Health check passed: {data['status']}")
                print(f"   OpenAI: {data['openai_client']}")
                print(f"   Auth: {data['authentication']}")
                return True
            else:
                print(f"❌ Health check failed: {response.text}")
                return False
        except Exception as e:
            print(f"❌ Health check error: {e}")
            return False
    
    def test_authentication(self):
        """Test authentication endpoint."""
        print("\n🔐 Testing authentication...")
        if not self.access_key:
            print("⚠️  No access key provided, skipping auth test")
            return False
            
        try:
            response = requests.post(
                f"{self.base_url}/auth",
                json={"access_key": self.access_key}
            )
            print(f"Status: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                if data.get("authenticated"):
                    self.token = data.get("token")
                    print(f"✅ Authentication successful")
                    print(f"   Token: {self.token[:10]}...")
                    return True
                else:
                    print(f"❌ Authentication failed: {data}")
                    return False
            else:
                print(f"❌ Authentication error: {response.text}")
                return False
        except Exception as e:
            print(f"❌ Authentication error: {e}")
            return False
    
    def test_models(self):
        """Test models endpoint."""
        print("\n📋 Testing models endpoint...")
        if not self.token:
            print("⚠️  No token available, skipping models test")
            return False
            
        try:
            headers = {"Authorization": f"Bearer {self.token}"}
            response = requests.get(f"{self.base_url}/models", headers=headers)
            print(f"Status: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Models retrieved successfully")
                print(f"   Count: {data.get('count', 'Unknown')}")
                return True
            else:
                print(f"❌ Models request failed: {response.text}")
                return False
        except Exception as e:
            print(f"❌ Models request error: {e}")
            return False
    
    def test_chat(self):
        """Test chat completion endpoint."""
        print("\n💬 Testing chat endpoint...")
        if not self.token:
            print("⚠️  No token available, skipping chat test")
            return False
            
        try:
            headers = {"Authorization": f"Bearer {self.token}"}
            payload = {
                "model": "gpt-3.5-turbo",
                "messages": [
                    {"role": "user", "content": "Say hello in one word"}
                ],
                "temperature": 0.7,
                "max_tokens": 10
            }
            response = requests.post(
                f"{self.base_url}/chat", 
                headers=headers, 
                json=payload
            )
            print(f"Status: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Chat completion successful")
                print(f"   Response: {data.get('message', 'No message')}")
                return True
            else:
                print(f"❌ Chat request failed: {response.text}")
                return False
        except Exception as e:
            print(f"❌ Chat request error: {e}")
            return False
    
    def test_completion(self):
        """Test text completion endpoint."""
        print("\n📝 Testing completion endpoint...")
        if not self.token:
            print("⚠️  No token available, skipping completion test")
            return False
            
        try:
            headers = {"Authorization": f"Bearer {self.token}"}
            payload = {
                "model": "gpt-3.5-turbo-instruct",
                "prompt": "The capital of France is",
                "temperature": 0.3,
                "max_tokens": 5
            }
            response = requests.post(
                f"{self.base_url}/completion", 
                headers=headers, 
                json=payload
            )
            print(f"Status: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Text completion successful")
                print(f"   Response: {data.get('text', 'No text')}")
                return True
            else:
                print(f"❌ Completion request failed: {response.text}")
                return False
        except Exception as e:
            print(f"❌ Completion request error: {e}")
            return False
    
    def test_embeddings(self):
        """Test embeddings endpoint."""
        print("\n🧮 Testing embeddings endpoint...")
        if not self.token:
            print("⚠️  No token available, skipping embeddings test")
            return False
            
        try:
            headers = {"Authorization": f"Bearer {self.token}"}
            payload = {
                "model": "text-embedding-ada-002",
                "input": "Hello world"
            }
            response = requests.post(
                f"{self.base_url}/embeddings", 
                headers=headers, 
                json=payload
            )
            print(f"Status: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                embeddings = data.get('embeddings', [])
                print(f"✅ Embeddings created successfully")
                print(f"   Dimensions: {len(embeddings[0]) if embeddings else 0}")
                return True
            else:
                print(f"❌ Embeddings request failed: {response.text}")
                return False
        except Exception as e:
            print(f"❌ Embeddings request error: {e}")
            return False
    
    def test_frontend(self):
        """Test frontend serving."""
        print("\n🌐 Testing frontend serving...")
        try:
            response = requests.get(self.base_url)
            print(f"Status: {response.status_code}")
            if response.status_code == 200:
                print(f"✅ Frontend served successfully")
                print(f"   Content length: {len(response.text)} characters")
                return True
            else:
                print(f"❌ Frontend serving failed: {response.text}")
                return False
        except Exception as e:
            print(f"❌ Frontend serving error: {e}")
            return False
    
    def run_all_tests(self):
        """Run all tests."""
        print("🚀 Starting Modular Backend Tests")
        print("=" * 50)
        
        results = {
            "health": self.test_health(),
            "frontend": self.test_frontend(),
            "auth": self.test_authentication(),
            "models": self.test_models(),
            "chat": self.test_chat(),
            "completion": self.test_completion(),
            "embeddings": self.test_embeddings(),
        }
        
        print("\n" + "=" * 50)
        print("📊 Test Results Summary")
        print("=" * 50)
        
        passed = sum(results.values())
        total = len(results)
        
        for test_name, result in results.items():
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"{test_name.upper():12} : {status}")
        
        print(f"\nTotal: {passed}/{total} tests passed")
        
        if passed == total:
            print("🎉 All tests passed! Modular backend is working correctly.")
        else:
            print("⚠️  Some tests failed. Check configuration and try again.")
        
        return results


def main():
    """Main test function."""
    print("🔧 Modular Backend Test Suite")
    print("This script tests the new modular architecture.")
    print()
    
    # Check if server is running
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        print(f"✅ Server is running at {BASE_URL}")
    except requests.exceptions.RequestException:
        print(f"❌ Server is not running at {BASE_URL}")
        print("Please start the server with: python main.py")
        return
    
    # Get access key from user or environment
    import os
    access_key = os.getenv("ACCESS_KEY") or input("\nEnter ACCESS_KEY (or press Enter to skip auth tests): ").strip()
    
    if not access_key:
        print("⚠️  No access key provided. Auth-required tests will be skipped.")
    
    # Run tests
    tester = BackendTester(BASE_URL, access_key or None)
    tester.run_all_tests()


if __name__ == "__main__":
    main() 