from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import os
from dotenv import load_dotenv

from rag.run_rag import query_rag

load_dotenv()
threshold = os.environ['threshold']

router = APIRouter()

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    reply: str
    
@router.post("/v1/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        reply = query_rag(request.message,threshold=float(threshold))
        if not reply:
            raise HTTPException(status_code=404, detail="No response found")
        return ChatResponse(reply=reply)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))