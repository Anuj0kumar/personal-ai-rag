from pydantic import BaseModel

class DocumentResponse(BaseModel):
    filename: str
    status: str
    user_id: str
    message: str
    content_preview: str # First 100 characters so you know it worked