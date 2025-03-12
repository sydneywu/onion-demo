from datetime import datetime, timedelta
from typing import Any, Union
from jose import jwt
from passlib.context import CryptContext
from src.config import settings

# Constants
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against a hash."""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Generate a password hash."""
    return pwd_context.hash(password)


def create_access_token(
    subject: Union[str, Any], 
    role_id: Union[str, Any], 
    tenant_id: Union[str, Any], 
    expires_delta: timedelta
) -> str:
    """Create a JWT access token."""
    expire = datetime.utcnow() + expires_delta
    to_encode = {
        "exp": expire, 
        "sub": str(subject), 
        "role_id": str(role_id), 
        "tenant_id": str(tenant_id)
    }
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt 