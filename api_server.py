"""
FastAPI server for external widget API access.
Provides REST endpoint for chat widget to communicate with AI assistant.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Tuple, Optional
import uvicorn

from core.chat import chat as chat_function

app = FastAPI(
    title="Career AI Assistant API",
    description="REST API for AI-powered career assistant chat widget",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str
    history: Optional[List[Tuple[str, str]]] = []

class ChatResponse(BaseModel):
    response: str
    status: str = "success"

@app.get("/")
async def root():
    return {
        "message": "Career AI Assistant API",
        "version": "1.0.0",
        "endpoints": {
            "chat": "/api/chat",
            "health": "/health"
        }
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/api/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """
    Main chat endpoint for widget communication.
    
    Args:
        request: ChatRequest with message and conversation history
        
    Returns:
        ChatResponse with AI assistant's reply
    """
    try:
        if not request.message or not request.message.strip():
            raise HTTPException(status_code=400, detail="Message cannot be empty")
        
        history_formatted = [
            {"role": "user", "content": msg[0]} if i % 2 == 0 
            else {"role": "assistant", "content": msg[1]}
            for i, msg in enumerate(request.history)
            for _ in [0, 1]
        ]
        
        response = chat_function(request.message, history_formatted)
        
        return ChatResponse(response=response, status="success")
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")

if __name__ == "__main__":
    print("🚀 Starting FastAPI server on http://127.0.0.1:8000")
    print("📖 API docs available at http://127.0.0.1:8000/docs")
    uvicorn.run(app, host="0.0.0.0", port=8000)