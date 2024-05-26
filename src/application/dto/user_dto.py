from pydantic import Field
from typing import Optional
from domain.models.user import UserBase

#remove id property for create
class UserRegistrationDTO(UserBase):
    id: Optional[int] = Field(None, exclude=True) 


class UserUpdateDto(UserBase):
    pass