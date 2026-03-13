from fastapi import APIRouter, Depends, HTTPException 
from app.schemas.chat import ChatRequest, ChatResponse
from app.services.ai_service import ai_service
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core import security
from app.models.chat_history import ChatMessage
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")
router = APIRouter()

async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, security.SECRET_KEY, algorithms=[security.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return username
    except JWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")
    
@router.post("/ask")
async def ask_ai(
    payload: ChatRequest, 
    current_user: str = Depends(get_current_user) 
):
    ai_reply, count = await ai_service.get_chat_response(
        session_id=current_user, 
        user_message=payload.message
    )
    
    return {"reply": ai_reply, "history_count": count}



@router.delete("/clear/{session_id}")
async def clear_chat_history(session_id: str, db: Session = Depends(get_db)):
    try:
        # 1. Find all messages for this session
        query = db.query(ChatMessage).filter(ChatMessage.session_id == session_id)
        
        # 2. Delete them
        count = query.delete(synchronize_session=False)
        db.commit()
        
        return {
            "status": "success",
            "message": f"Deleted {count} messages for session {session_id}",
            "session_id": session_id
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to clear history: {str(e)}")