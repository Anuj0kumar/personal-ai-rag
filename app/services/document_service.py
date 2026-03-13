import os
from pypdf import PdfReader
from fastapi import UploadFile

class DocumentService:
    def __init__(self):
        self.upload_dir = "uploads"
        # Ensure the folder exists
        if not os.path.exists(self.upload_dir):
            os.makedirs(self.upload_dir)

    async def process_pdf(self, file: UploadFile) -> str:
        # 1. Save the file temporarily
        file_path = os.path.join(self.upload_dir, file.filename)
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)

        # 2. Extract Text
        reader = PdfReader(file_path)
        extracted_text = ""
        for page in reader.pages:
            extracted_text += page.extract_text() + "\n"
        
        return extracted_text

document_service = DocumentService()