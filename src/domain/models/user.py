from typing import Optional

from pydantic import BaseModel
from datetime import datetime

class UserBase(BaseModel):
    id: Optional[int] = None
    username: str
    email: str
    hashed_password: str

class User(UserBase):
    created_at: Optional[datetime] = None
    created_by: Optional[int] = None
    updated_at: Optional[datetime] = None
    updated_by: Optional[int] = None
    deleted_at: Optional[datetime] = None
    deleted_by: Optional[datetime] = None