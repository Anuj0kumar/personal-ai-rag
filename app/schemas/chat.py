from pydantic import BaseModel

class Message(BaseModel):
    role: str  # "user" or "assistant"
    content: str

class ChatRequest(BaseModel):
    message: str
    session_id: str  # Unique ID for the conversation

class ChatResponse(BaseModel):
    reply: str
    history_count: int