from typing import Optional
from pydantic import BaseModel


class Login(BaseModel):
    email: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    sub: Optional[int] = None
    role_id: Optional[int] = None
    tenant_id: Optional[int] = None 