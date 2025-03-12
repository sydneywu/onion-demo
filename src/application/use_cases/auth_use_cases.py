from domain.repositories.auth_repository import AuthRepository
from domain.models.auth import Login, Token
from application.dto.auth_dto import UserLoginDTO


class AuthUseCases:
    def __init__(self, auth_repository: AuthRepository):
        self.auth_repository = auth_repository

    async def login_access_token(self, form_data: UserLoginDTO) -> Token:
        """
        Authenticate a user and return an access token.
        """
        login = Login(email=form_data.email, password=form_data.password)
        token = await self.auth_repository.login_access_token(login)
        return token 