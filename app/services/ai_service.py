import openai
from ..core.config import settings
from app.services.vector_service import vector_service
from app.core.database import SessionLocal
from app.models.chat_history import ChatMessage

class AIService:
    def __init__(self):
        # Local Ollama Configuration
        self.client = openai.AsyncOpenAI(
            base_url="http://localhost:11434/v1", 
            api_key="ollama" 
        )
        # In-memory history (Session ID -> List of Messages)
        self.history_db = {}
        
    def clear_local_memory(self, session_id: str):
        if session_id in self.history_db:
            del self.history_db[session_id]

    def _trim_history(self, session_id: str, limit: int = 10):
        """Keep the history from growing too large for the local model."""
        if session_id in self.history_db and len(self.history_db[session_id]) > limit:
            system_msg = self.history_db[session_id][0]
            # Keep the last 'limit-1' messages
            recent_msgs = self.history_db[session_id][-(limit-1):]
            self.history_db[session_id] = [system_msg] + recent_msgs

    async def get_chat_response(self, session_id: str, user_message: str):
        db = SessionLocal()
        try:
            # 1. RETRIEVE history from SQL instead of dict
            past_messages = db.query(ChatMessage).filter(
                ChatMessage.session_id == session_id
            ).order_by(ChatMessage.timestamp.asc()).all()

            # Format for the AI
            history = [{"role": msg.role, "content": msg.content} for msg in past_messages]

            # 2. SEARCH Vector DB for context
            context = await vector_service.search_docs(user_message, user_id=session_id)
            
            system_prompt = {"role": "system", "content": f"Use this context: {context}"}
            
            # 3. BUILD message list (System + History + New Message)
            messages = [system_prompt] + history + [{"role": "user", "content": user_message}]

            # 4. GENERATE
            response = await self.client.chat.completions.create(
                model="llama3",
                messages=messages
            )
            ai_reply = response.choices[0].message.content

            # 5. SAVE both messages to SQL
            user_entry = ChatMessage(session_id=session_id, role="user", content=user_message)
            ai_entry = ChatMessage(session_id=session_id, role="assistant", content=ai_reply)
            
            db.add(user_entry)
            db.add(ai_entry)
            db.commit()

            return ai_reply, len(history) + 2

        finally:
            db.close()

# Create a single instance to be used by the FastAPI routes
ai_service = AIService()