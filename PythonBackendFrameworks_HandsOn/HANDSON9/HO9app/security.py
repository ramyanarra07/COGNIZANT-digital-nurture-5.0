from datetime import datetime, timedelta, timezone
from typing import Optional
from passlib.context import CryptContext
from jose import jwt

# 87. Initialize CryptContext with the bcrypt hashing algorithm
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT Configuration Parameters
SECRET_KEY = "super-secret-key-that-should-be-kept-hidden-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# --- 87 & 89. Password Hashing Operations ---
def get_password_hash(password: str) -> str:
    """
    89. Generates a secure bcrypt hash of a plain text string.
    Bcrypt intentionally uses a high computational work factor to resist brute-force attacks,
    unlike MD5 or SHA-256 which are fast and highly vulnerable to precomputed rainbow tables.
    """
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifies a plain text password against a recorded bcrypt hash."""
    return pwd_context.verify(plain_password, hashed_password)

# --- 91. JWT Generation Utilities ---
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)