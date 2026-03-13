from fastapi import APIRouter, UploadFile, File, HTTPException , Depends
from app.services.document_service import document_service
from app.schemas.document import DocumentResponse
from app.services.vector_service import vector_service
from .chat import get_current_user

router = APIRouter()

@router.post("/pdf", response_model=DocumentResponse)
async def upload_pdf(
    file: UploadFile = File(...),
    current_user: str = Depends(get_current_user) # Automatically gets username from token
):
    try:
        text = await document_service.process_pdf(file)
        # Use current_user as the user_id automatically
        num_chunks = await vector_service.add_text_to_index(text, file.filename, current_user)
        
        return {
            "filename": file.filename,
            "user_id": current_user,
            "status": "success",
            "message": f"Indexed {num_chunks} chunks successfully",
            "content_preview": text[:100] + "..."
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))