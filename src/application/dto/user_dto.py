from pydantic import BaseModel

class UserRegistrationDTO(BaseModel):
    username: str
    email: str
    password: str