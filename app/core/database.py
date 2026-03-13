from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .config import settings

# Use the DATABASE_URL from your .env or a local sqlite file
SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL or "sqlite:///./sql_app.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()