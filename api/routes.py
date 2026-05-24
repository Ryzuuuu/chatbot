from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
import uuid
from api.session_store import get_session, delete_session

router = APIRouter()

class ChatRequest(BaseModel):
    session_id: Optional[str] = None
    message: str

class ChatResponse(BaseModel):
    session_id: str
    reply: str
    turn_count: int

@router.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    sid = req.session_id or str(uuid.uuid4())
    bot = get_session(sid)
    reply = bot.chat(req.message)
    return ChatResponse(
        session_id=sid,
        reply=reply,
        turn_count=len(bot.get_history()) // 2
    )

@router.delete("/chat/{session_id}")
def clear(session_id: str):
    delete_session(session_id)
    return {"status": "cleared"}

@router.get("/chat/{session_id}/history")
def history(session_id: str):
    bot = get_session(session_id)
    msgs = bot.get_history()
    return {"messages": [{"role": m.type, "content": m.content} for m in msgs]}

@router.get("/health")
def health():
    return {"status": "ok"}