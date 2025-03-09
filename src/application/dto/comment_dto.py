from pydantic import Field
from typing import Optional
from domain.models.comment import CommentBase

# Remove id property for create
class CommentCreateDTO(CommentBase):
    id: Optional[int] = Field(None, exclude=True)


class CommentUpdateDTO(CommentBase):
    name: Optional[str] = None
    description: Optional[str] = None
    user_id: Optional[int] = None 