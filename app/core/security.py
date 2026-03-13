from datetime import datetime, timedelta, timezone
from jose import jwt
from passlib.context import CryptContext

# Configuration
SECRET_KEY = "your-very-secret-key-change-this" 
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Using argon2 to avoid the bcrypt 72-byte limit bug
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

def get_password_hash(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

# THIS IS THE FUNCTION YOUR ERROR IS COMPLAINING ABOUT
def create_access_token(data: dict):
    to_encode = data.copy()
    # 2026 Best Practice: Use timezone-aware UTC
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt