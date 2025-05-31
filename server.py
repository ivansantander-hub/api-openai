from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from typing import List, Optional
import openai
import os
import uuid

# Load environment variables from .env file
load_dotenv()

app = FastAPI(
    title="OpenAI API Service",
    description="A comprehensive FastAPI service for OpenAI integrations",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Get API key from environment variables
api_key = os.getenv('OPENAI_API_KEY')

if not api_key:
    print("⚠️  WARNING: OpenAI API key is not configured.")
    print("   Create a .env file with: OPENAI_API_KEY=your_key_here")
    print("   The server will start but OpenAI endpoints will return errors.")
    client = None
else:
    # Initialize OpenAI client with new simple initialization
    try:
        client = openai.OpenAI(api_key=api_key)
        print("✅ OpenAI client initialized successfully")
    except Exception as e:
        print(f"❌ Warning: Could not initialize OpenAI client: {e}")
        print("   The server will start but OpenAI endpoints will not work.")
        client = None

# Pydantic models
class Message(BaseModel):
    role: str = Field(..., description="Role of the message (user, assistant, system)")
    content: str = Field(..., description="Content of the message")

class ChatRequest(BaseModel):
    messages: List[Message] = Field(..., description="List of messages for the conversation")
    model: str = Field(default="gpt-3.5-turbo", description="OpenAI model to use")
    temperature: float = Field(default=0.7, ge=0, le=2, description="Temperature for response generation")
    max_tokens: Optional[int] = Field(default=None, description="Maximum tokens in response")

class CompletionRequest(BaseModel):
    prompt: str = Field(..., description="Text prompt for completion")
    model: str = Field(default="gpt-3.5-turbo-instruct", description="OpenAI model to use")
    temperature: float = Field(default=0.7, ge=0, le=2, description="Temperature for response generation")
    max_tokens: Optional[int] = Field(default=100, description="Maximum tokens in response")

class ImageRequest(BaseModel):
    prompt: str = Field(..., description="Description of the image to generate")
    size: str = Field(default="1024x1024", description="Size of the generated image")
    quality: str = Field(default="standard", description="Quality of the generated image")
    n: int = Field(default=1, ge=1, le=10, description="Number of images to generate")

class EmbeddingRequest(BaseModel):
    text: str = Field(..., description="Text to generate embeddings for")
    model: str = Field(default="text-embedding-ada-002", description="Embedding model to use")

class TranscriptionRequest(BaseModel):
    language: Optional[str] = Field(default=None, description="Language of the audio")
    response_format: str = Field(default="json", description="Response format")

# Response models
class ChatResponse(BaseModel):
    id: str
    message: str
    model: str
    usage: dict

class CompletionResponse(BaseModel):
    id: str
    text: str
    model: str
    usage: dict

class ImageResponse(BaseModel):
    id: str
    urls: List[str]
    revised_prompts: Optional[List[str]] = None

class EmbeddingResponse(BaseModel):
    id: str
    embeddings: List[List[float]]
    model: str
    usage: dict

class HealthResponse(BaseModel):
    status: str
    message: str

# Helper function to check if OpenAI client is available
def check_openai_client():
    if client is None:
        raise HTTPException(
            status_code=503, 
            detail="OpenAI client is not initialized. Please check your API key configuration."
        )

# Endpoints
@app.get("/", response_model=HealthResponse)
async def root():
    """Root endpoint to check if the API is running"""
    return HealthResponse(status="ok", message="OpenAI API Service is running")

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    openai_status = "available" if client is not None else "unavailable"
    return HealthResponse(
        status="healthy", 
        message=f"Service is operational. OpenAI client: {openai_status}"
    )

@app.post("/chat", response_model=ChatResponse)
async def chat_completion(request: ChatRequest):
    """Generate chat completions using OpenAI's chat models"""
    check_openai_client()
    
    try:
        response = client.chat.completions.create(
            model=request.model,
            messages=[{"role": msg.role, "content": msg.content} for msg in request.messages],
            temperature=request.temperature,
            max_tokens=request.max_tokens
        )
        
        return ChatResponse(
            id=str(uuid.uuid4()),
            message=response.choices[0].message.content,
            model=response.model,
            usage=response.usage.model_dump()
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating chat completion: {str(e)}")

@app.post("/completion", response_model=CompletionResponse)
async def text_completion(request: CompletionRequest):
    """Generate text completions using OpenAI's completion models"""
    check_openai_client()
    
    try:
        response = client.completions.create(
            model=request.model,
            prompt=request.prompt,
            temperature=request.temperature,
            max_tokens=request.max_tokens
        )
        
        return CompletionResponse(
            id=str(uuid.uuid4()),
            text=response.choices[0].text,
            model=response.model,
            usage=response.usage.model_dump()
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating completion: {str(e)}")

@app.post("/images/generate", response_model=ImageResponse)
async def generate_image(request: ImageRequest):
    """Generate images using DALL-E"""
    check_openai_client()
    
    try:
        response = client.images.generate(
            model="dall-e-3",
            prompt=request.prompt,
            size=request.size,
            quality=request.quality,
            n=request.n
        )
        
        urls = [img.url for img in response.data]
        revised_prompts = [img.revised_prompt for img in response.data if hasattr(img, 'revised_prompt')]
        
        return ImageResponse(
            id=str(uuid.uuid4()),
            urls=urls,
            revised_prompts=revised_prompts if revised_prompts else None
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating image: {str(e)}")

@app.post("/embeddings", response_model=EmbeddingResponse)
async def create_embedding(request: EmbeddingRequest):
    """Generate embeddings for text"""
    check_openai_client()
    
    try:
        response = client.embeddings.create(
            model=request.model,
            input=request.text
        )
        
        return EmbeddingResponse(
            id=str(uuid.uuid4()),
            embeddings=[data.embedding for data in response.data],
            model=response.model,
            usage=response.usage.model_dump()
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating embedding: {str(e)}")

@app.get("/models")
async def list_models():
    """List available OpenAI models"""
    check_openai_client()
    
    try:
        response = client.models.list()
        return {"models": [model.id for model in response.data]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching models: {str(e)}")

if __name__ == '__main__':
    import uvicorn
    print("\n🚀 Starting OpenAI API Service...")
    print("📖 Documentation: http://localhost:8000/docs")
    print("❤️  Health Check: http://localhost:8000/health")
    print("🔑 Make sure to set OPENAI_API_KEY in .env file")
    uvicorn.run(app, host='0.0.0.0', port=8000)
