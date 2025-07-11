from fastapi import FastAPI, HTTPException, Depends, Header
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from typing import List, Optional, Annotated
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

# Mount static files (web client)
app.mount("/static", StaticFiles(directory="public"), name="static")

# Get API key from environment variables
api_key = os.getenv('OPENAI_API_KEY')

# Get authentication key from environment variables
auth_key = os.getenv('ACCESS_KEY')

if not auth_key:
    print("⚠️  WARNING: ACCESS_KEY is not configured.")
    print("   Set ACCESS_KEY environment variable in Railway")
    print("   Users will not be able to authenticate.")

if not api_key:
    print("⚠️  WARNING: OpenAI API key is not configured.")
    print("   Create a .env file with: OPENAI_API_KEY=your_api_key_here")
    print("   The server will start but OpenAI endpoints will return 503 errors.")
    client = None
else:
    try:
        # Initialize OpenAI client with proper error handling
        client = openai.OpenAI(api_key=api_key)
        print("✅ OpenAI client initialized successfully")
    except Exception as e:
        print(f"❌ Error initializing OpenAI client: {e}")
        client = None

# Security scheme
security = HTTPBearer(auto_error=False)

# Request/Response Models
class AuthRequest(BaseModel):
    access_key: str = Field(..., description="Access key for authentication")

class AuthResponse(BaseModel):
    authenticated: bool = Field(..., description="Authentication status")
    message: str = Field(..., description="Authentication message")
    token: Optional[str] = Field(None, description="Authentication token")

class ChatMessage(BaseModel):
    role: str = Field(..., description="Role of the message sender")
    content: str = Field(..., description="Content of the message")

class ChatRequest(BaseModel):
    model: str = Field(default="gpt-3.5-turbo", description="Model to use for chat completion")
    messages: List[ChatMessage] = Field(..., description="List of messages in the conversation")
    temperature: Optional[float] = Field(default=0.7, ge=0, le=2, description="Sampling temperature")
    max_tokens: Optional[int] = Field(default=1000, gt=0, description="Maximum number of tokens to generate")

class CompletionRequest(BaseModel):
    model: str = Field(default="gpt-3.5-turbo-instruct", description="Model to use for completion")
    prompt: str = Field(..., description="The prompt to complete")
    temperature: Optional[float] = Field(default=0.7, ge=0, le=2, description="Sampling temperature")
    max_tokens: Optional[int] = Field(default=100, gt=0, description="Maximum number of tokens to generate")

class ImageRequest(BaseModel):
    prompt: str = Field(..., description="Text description of the desired image")
    size: Optional[str] = Field(default="1024x1024", description="Size of the generated image")
    quality: Optional[str] = Field(default="standard", description="Quality of the generated image")
    n: Optional[int] = Field(default=1, ge=1, le=4, description="Number of images to generate")

class EmbeddingRequest(BaseModel):
    model: str = Field(default="text-embedding-ada-002", description="Model to use for embeddings")
    input: str = Field(..., description="Text to create embeddings for")

# Helper function to check authentication
def verify_access_key(credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)):
    if not auth_key:
        raise HTTPException(
            status_code=503,
            detail="Authentication not configured. Please set ACCESS_KEY."
        )
    
    if not credentials:
        raise HTTPException(
            status_code=401,
            detail="Authentication required. Please provide access key."
        )
    
    if credentials.credentials != auth_key:
        raise HTTPException(
            status_code=403,
            detail="Invalid access key."
        )
    
    return credentials.credentials

# Helper function to check if OpenAI client is available
def check_openai_client():
    if client is None:
        raise HTTPException(
            status_code=503,
            detail="OpenAI client not available. Please configure OPENAI_API_KEY."
        )

# Routes

@app.get("/")
async def root():
    """Serve the web client interface"""
    return FileResponse('public/index.html')

@app.post("/auth")
async def authenticate(request: AuthRequest):
    """Authenticate user with access key"""
    if not auth_key:
        raise HTTPException(
            status_code=503,
            detail="Authentication not configured. Please set ACCESS_KEY."
        )
    
    if request.access_key == auth_key:
        return AuthResponse(
            authenticated=True,
            message="Authentication successful",
            token=request.access_key  # In a real app, you'd generate a JWT token
        )
    else:
        raise HTTPException(
            status_code=403,
            detail="Invalid access key"
        )

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    openai_status = "available" if client is not None else "unavailable"
    auth_status = "configured" if auth_key else "not configured"
    
    return {
        "status": "healthy",
        "message": f"Service is operational. OpenAI client: {openai_status}",
        "openai_client": openai_status,
        "authentication": auth_status,
        "service_version": "1.0.0"
    }

@app.post("/chat")
async def chat_completion(request: ChatRequest, token: str = Depends(verify_access_key)):
    """Generate chat completion using OpenAI"""
    check_openai_client()
    
    try:
        response = client.chat.completions.create(
            model=request.model,
            messages=[{"role": msg.role, "content": msg.content} for msg in request.messages],
            temperature=request.temperature,
            max_tokens=request.max_tokens
        )
        
        return {
            "message": response.choices[0].message.content,
            "model": request.model,
            "usage": response.usage.model_dump() if response.usage else None,
            "id": response.id
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"OpenAI API error: {str(e)}")

@app.post("/completion")
async def text_completion(request: CompletionRequest, token: str = Depends(verify_access_key)):
    """Generate text completion using OpenAI"""
    check_openai_client()
    
    try:
        response = client.completions.create(
            model=request.model,
            prompt=request.prompt,
            temperature=request.temperature,
            max_tokens=request.max_tokens
        )
        
        return {
            "text": response.choices[0].text,
            "model": request.model,
            "usage": response.usage.model_dump() if response.usage else None,
            "id": response.id
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"OpenAI API error: {str(e)}")

@app.post("/images/generate")
async def generate_image(request: ImageRequest, token: str = Depends(verify_access_key)):
    """Generate image using DALL-E"""
    check_openai_client()
    
    try:
        response = client.images.generate(
            model="dall-e-3",
            prompt=request.prompt,
            size=request.size,
            quality=request.quality,
            n=request.n
        )
        
        return {
            "url": response.data[0].url,
            "prompt": request.prompt,
            "size": request.size,
            "quality": request.quality,
            "revised_prompt": response.data[0].revised_prompt if hasattr(response.data[0], 'revised_prompt') else None
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"OpenAI API error: {str(e)}")

@app.post("/embeddings")
async def create_embeddings(request: EmbeddingRequest, token: str = Depends(verify_access_key)):
    """Create embeddings using OpenAI"""
    check_openai_client()
    
    try:
        response = client.embeddings.create(
            model=request.model,
            input=request.input
        )
        
        return {
            "embeddings": [data.embedding for data in response.data],
            "model": request.model,
            "usage": response.usage.model_dump() if response.usage else None
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"OpenAI API error: {str(e)}")

@app.get("/models")
async def list_models(token: str = Depends(verify_access_key)):
    """List available OpenAI models"""
    check_openai_client()
    
    try:
        response = client.models.list()
        models = [model.model_dump() for model in response.data]
        
        return {
            "models": models,
            "count": len(models)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"OpenAI API error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting OpenAI API Service...")
    print("📡 Server will be available at: http://localhost:8000")
    print("🌐 Web Client will be available at: http://localhost:8000")
    print("📚 API Documentation at: http://localhost:8000/docs")
    uvicorn.run(app, host="0.0.0.0", port=8000)
