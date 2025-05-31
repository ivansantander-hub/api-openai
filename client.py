import requests
import json
from typing import List, Dict, Optional
from dataclasses import dataclass

@dataclass
class ApiClient:
    """Basic client to interact with the OpenAI API Service"""
    
    base_url: str = "http://localhost:8000"
    
    def _make_request(self, method: str, endpoint: str, data: Optional[Dict] = None) -> Dict:
        """Make HTTP request to the API"""
        url = f"{self.base_url}{endpoint}"
        
        try:
            if method.upper() == "GET":
                response = requests.get(url)
            elif method.upper() == "POST":
                response = requests.post(url, json=data)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
            
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            print(f"Error making request to {url}: {e}")
            raise
    
    def health_check(self) -> Dict:
        """Check if the API service is healthy"""
        return self._make_request("GET", "/health")
    
    def chat_completion(self, messages: List[Dict], model: str = "gpt-3.5-turbo", 
                       temperature: float = 0.7, max_tokens: Optional[int] = None) -> Dict:
        """Generate chat completion"""
        data = {
            "messages": messages,
            "model": model,
            "temperature": temperature
        }
        if max_tokens:
            data["max_tokens"] = max_tokens
            
        return self._make_request("POST", "/chat", data)
    
    def text_completion(self, prompt: str, model: str = "gpt-3.5-turbo-instruct",
                       temperature: float = 0.7, max_tokens: int = 100) -> Dict:
        """Generate text completion"""
        data = {
            "prompt": prompt,
            "model": model,
            "temperature": temperature,
            "max_tokens": max_tokens
        }
        return self._make_request("POST", "/completion", data)
    
    def generate_image(self, prompt: str, size: str = "1024x1024", 
                      quality: str = "standard", n: int = 1) -> Dict:
        """Generate images using DALL-E"""
        data = {
            "prompt": prompt,
            "size": size,
            "quality": quality,
            "n": n
        }
        return self._make_request("POST", "/images/generate", data)
    
    def create_embedding(self, text: str, model: str = "text-embedding-ada-002") -> Dict:
        """Create embeddings for text"""
        data = {
            "text": text,
            "model": model
        }
        return self._make_request("POST", "/embeddings", data)
    
    def list_models(self) -> Dict:
        """List available OpenAI models"""
        return self._make_request("GET", "/models")


def main():
    """Example usage of the API client"""
    client = ApiClient()
    
    print("🚀 Testing OpenAI API Service Client")
    print("=" * 50)
    
    # Health check
    try:
        health = client.health_check()
        print(f"✅ Health Check: {health['status']} - {health['message']}")
    except Exception as e:
        print(f"❌ Health Check Failed: {e}")
        return
    
    # Test chat completion
    try:
        print("\n💬 Testing Chat Completion...")
        messages = [
            {"role": "user", "content": "Hello! Tell me a short joke."}
        ]
        chat_response = client.chat_completion(messages)
        print(f"Response: {chat_response['message']}")
        print(f"Model: {chat_response['model']}")
    except Exception as e:
        print(f"❌ Chat Completion Failed: {e}")
    
    # Test text completion
    try:
        print("\n📝 Testing Text Completion...")
        completion_response = client.text_completion("The future of AI is")
        print(f"Completion: {completion_response['text']}")
    except Exception as e:
        print(f"❌ Text Completion Failed: {e}")
    
    # Test embeddings
    try:
        print("\n🔢 Testing Embeddings...")
        embedding_response = client.create_embedding("Hello world")
        print(f"Embedding vector length: {len(embedding_response['embeddings'][0])}")
    except Exception as e:
        print(f"❌ Embeddings Failed: {e}")
    
    # Test image generation (commented out as it may take time)
    # try:
    #     print("\n🎨 Testing Image Generation...")
    #     image_response = client.generate_image("A cute cat wearing sunglasses")
    #     print(f"Generated {len(image_response['urls'])} image(s)")
    #     print(f"Image URL: {image_response['urls'][0]}")
    # except Exception as e:
    #     print(f"❌ Image Generation Failed: {e}")
    
    # List models
    try:
        print("\n📋 Testing List Models...")
        models_response = client.list_models()
        print(f"Available models: {len(models_response['models'])} found")
        print("First 5 models:", models_response['models'][:5])
    except Exception as e:
        print(f"❌ List Models Failed: {e}")


if __name__ == "__main__":
    main() 