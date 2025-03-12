from abc import ABC, abstractmethod
from domain.models.auth import Login, Token


class AuthRepository(ABC):
    @abstractmethod
    async def login_access_token(self, form_data: Login) -> Token:
        pass 