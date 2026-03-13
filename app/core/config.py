from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    # 1. Matches OPENAI_API_KEY in .env
    OPENAI_API_KEY: str
    
    # 2. Add a default or make it Optional so it doesn't crash without a DB
    DATABASE_URL: Optional[str] = None 
    
    # 3. Matches VECTOR_DB_PATH in .env
    VECTOR_DB_PATH: str = "./data/chroma"
    
    # 4. Matches PROJECT_NAME in .env (Ensure case matches exactly!)
    PROJECT_NAME: str = "AI Knowledge API"

    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding='utf-8',
        extra='ignore'  # This prevents the "Extra inputs" error if you have extra stuff in .env
    )

settings = Settings()