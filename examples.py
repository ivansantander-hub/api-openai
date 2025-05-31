"""
Advanced examples demonstrating various use cases of the OpenAI API Service
"""

from client import ApiClient
import time
import json

def example_conversation():
    """Example: Multi-turn conversation"""
    print("🗣️  Multi-turn Conversation Example")
    print("-" * 40)
    
    client = ApiClient()
    
    # Start conversation
    messages = [
        {"role": "system", "content": "You are a helpful assistant that explains programming concepts."},
        {"role": "user", "content": "What is Python?"}
    ]
    
    # First response
    response1 = client.chat_completion(messages)
    print(f"User: What is Python?")
    print(f"AI: {response1['message'][:100]}...")
    
    # Continue conversation
    messages.append({"role": "assistant", "content": response1['message']})
    messages.append({"role": "user", "content": "Can you give me a simple example?"})
    
    response2 = client.chat_completion(messages)
    print(f"\nUser: Can you give me a simple example?")
    print(f"AI: {response2['message'][:100]}...")


def example_creative_writing():
    """Example: Creative writing with different temperatures"""
    print("\n✍️  Creative Writing with Different Temperatures")
    print("-" * 50)
    
    client = ApiClient()
    prompt = "Write a short story about a robot learning to paint."
    
    temperatures = [0.2, 0.7, 1.5]
    
    for temp in temperatures:
        print(f"\n🌡️  Temperature: {temp}")
        response = client.text_completion(
            prompt=prompt,
            temperature=temp,
            max_tokens=150
        )
        print(f"Story: {response['text'][:100]}...")


def example_embeddings_similarity():
    """Example: Text similarity using embeddings"""
    print("\n🔍 Text Similarity using Embeddings")
    print("-" * 40)
    
    client = ApiClient()
    
    texts = [
        "I love programming in Python",
        "Python is my favorite programming language",
        "I enjoy cooking Italian food",
        "Pasta is delicious"
    ]
    
    embeddings = []
    for text in texts:
        response = client.create_embedding(text)
        embeddings.append(response['embeddings'][0])
        print(f"Generated embedding for: '{text}'")
    
    # Simple similarity calculation (dot product)
    def cosine_similarity(a, b):
        dot_product = sum(x * y for x, y in zip(a, b))
        magnitude_a = sum(x ** 2 for x in a) ** 0.5
        magnitude_b = sum(x ** 2 for x in b) ** 0.5
        return dot_product / (magnitude_a * magnitude_b)
    
    print("\n📊 Similarity Matrix:")
    for i, text1 in enumerate(texts):
        for j, text2 in enumerate(texts):
            if i != j:
                similarity = cosine_similarity(embeddings[i], embeddings[j])
                print(f"'{text1[:20]}...' vs '{text2[:20]}...': {similarity:.3f}")


def example_batch_processing():
    """Example: Batch processing multiple requests"""
    print("\n⚡ Batch Processing Example")
    print("-" * 30)
    
    client = ApiClient()
    
    questions = [
        "What is machine learning?",
        "Explain quantum computing",
        "What is blockchain?",
        "Define artificial intelligence"
    ]
    
    print("Processing multiple questions...")
    responses = []
    
    for i, question in enumerate(questions, 1):
        print(f"Processing {i}/{len(questions)}: {question}")
        
        response = client.chat_completion([
            {"role": "user", "content": f"In one sentence, {question.lower()}"}
        ])
        responses.append({
            "question": question,
            "answer": response['message'],
            "model": response['model']
        })
        
        # Small delay to avoid rate limiting
        time.sleep(0.5)
    
    print("\n📋 Results Summary:")
    for item in responses:
        print(f"Q: {item['question']}")
        print(f"A: {item['answer'][:80]}...")
        print()


def example_image_generation_variants():
    """Example: Generate image variations"""
    print("\n🎨 Image Generation Variants")
    print("-" * 35)
    
    client = ApiClient()
    
    base_prompt = "A futuristic city"
    styles = [
        "in cyberpunk style",
        "in watercolor painting style", 
        "in pixel art style",
        "in minimalist design"
    ]
    
    print(f"Base prompt: '{base_prompt}'")
    print("Generating variations...")
    
    for style in styles:
        full_prompt = f"{base_prompt} {style}"
        print(f"\nGenerating: {full_prompt}")
        
        try:
            response = client.generate_image(
                prompt=full_prompt,
                size="1024x1024",
                quality="standard"
            )
            print(f"✅ Generated image: {response['urls'][0]}")
            if response.get('revised_prompts'):
                print(f"📝 Revised prompt: {response['revised_prompts'][0][:60]}...")
        except Exception as e:
            print(f"❌ Error: {e}")
        
        # Delay to avoid rate limiting
        time.sleep(2)


def example_model_comparison():
    """Example: Compare responses from different models"""
    print("\n🤖 Model Comparison")
    print("-" * 25)
    
    client = ApiClient()
    
    # First, let's see available models
    try:
        models_response = client.list_models()
        chat_models = [m for m in models_response['models'] if 'gpt' in m.lower()]
        print(f"Available GPT models: {chat_models[:3]}")
    except:
        chat_models = ["gpt-3.5-turbo"]  # fallback
    
    question = "Explain the concept of recursion in programming"
    print(f"\nQuestion: {question}")
    
    for model in chat_models[:2]:  # Test first 2 models
        try:
            print(f"\n🔄 Testing model: {model}")
            response = client.chat_completion(
                messages=[{"role": "user", "content": question}],
                model=model,
                temperature=0.7,
                max_tokens=100
            )
            print(f"Response: {response['message'][:80]}...")
            print(f"Tokens used: {response['usage']}")
        except Exception as e:
            print(f"❌ Error with {model}: {e}")


def main():
    """Run all examples"""
    print("🚀 OpenAI API Service - Advanced Examples")
    print("=" * 50)
    
    examples = [
        example_conversation,
        example_creative_writing,
        example_embeddings_similarity,
        example_batch_processing,
        # example_image_generation_variants,  # Commented due to cost
        example_model_comparison
    ]
    
    for example_func in examples:
        try:
            example_func()
            time.sleep(1)  # Brief pause between examples
        except Exception as e:
            print(f"❌ Error in {example_func.__name__}: {e}")
    
    print("\n🎉 All examples completed!")


if __name__ == "__main__":
    main() 