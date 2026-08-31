from pydantic import BaseModel
from typing import List, Optional

class MessageHistory(BaseModel):
    text: str
    is_user: bool

class ChatRequest(BaseModel):
    email: str = "user@example.com"
    message: str
    history: Optional[List[MessageHistory]] = []

class ChatResponse(BaseModel):
    reply: str
    risk_score: int
    risk_breakdown: dict
