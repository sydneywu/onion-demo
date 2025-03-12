from typing import List

from domain.models.user import User
from domain.repositories.user_repository import UserRepository
from application.dto.user_dto import UserRegistrationDTO
from utils.security import get_password_hash


class UserUseCases:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def register(self, user_dto: UserRegistrationDTO) -> User:
        # Hash the password using the security utility
        hashed_password = get_password_hash(user_dto.password)

        user = User(username=user_dto.username, email=user_dto.email, hashed_password=hashed_password)
        await self.user_repository.add(user)
        return user

    async def get_all(self) -> List[User]:
        users = await self.user_repository.get_all()
        return users