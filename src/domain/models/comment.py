from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class CommentBase(BaseModel):
    id: Optional[int] = None
    name: str
    description: str
    user_id: int

class Comment(CommentBase):
    created_at: Optional[datetime] = None
    created_by: Optional[int] = None
    updated_at: Optional[datetime] = None
    updated_by: Optional[int] = None
    is_deleted: bool = False
    deleted_at: Optional[datetime] = None
    deleted_by: Optional[int] = None 