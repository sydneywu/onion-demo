from pydantic import BaseModel, Field
from typing import Optional
from domain.models.user import UserBase

#remove id property for create
class UserRegistrationDTO(BaseModel):
    username: str
    email: str
    password: str


class UserUpdateDto(UserBase):
    pass