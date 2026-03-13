from fastapi import FastAPI
from app.api.endpoints import auth, chat ,upload 
from app.core.database import engine
from app.models import chat_history, user
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

app = FastAPI(title="AI Knowledge API")

app.mount("/static", StaticFiles(directory="static", html=True), name="static")

chat_history.Base.metadata.create_all(bind=engine)
user.Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins (good for local testing)
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

# Include our routers
app.include_router(chat.router, prefix="/ai", tags=["Chat"])
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(upload.router, prefix="/documents", tags=["Upload"])



@app.get("/")
async def root():
    return {"message": "AI API is Online"}
