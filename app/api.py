from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from rag.run_rag import query_rag

router = APIRouter()

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    reply: str
    
@router.post("/v1/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        reply = query_rag(request.message)
        return ChatResponse(reply=reply)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))