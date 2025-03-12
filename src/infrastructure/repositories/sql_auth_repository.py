import datetime
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from domain.models.auth import Login, Token
from domain.repositories.auth_repository import AuthRepository
from infrastructure.orm.user_orm_model import UserOrmModel
from utils.security import verify_password, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES


class SQLAuthRepository(AuthRepository):
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def login_access_token(self, form_data: Login) -> Token:
        """
        Authenticate a user and return an access token.
        """
        # Query the user by email
        result = await self.db_session.execute(select(UserOrmModel).filter(UserOrmModel.email == form_data.email))
        orm_user = result.scalars().first()
        
        if orm_user is None:
            raise HTTPException(status_code=400, detail="Wrong User")
            
        if not verify_password(form_data.password, orm_user.hashed_password):
            raise HTTPException(status_code=400, detail="Wrong Email / Password")

        user = orm_user.to_domain()

        # For now, we'll use placeholder values for role_id and tenant_id
        # In a real application, you would query these from the database
        role_id = 1  # Default role
        tenant_id = 1  # Default tenant
            
        # Create and return JWT token
        access_token_expires = datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        return Token(
            access_token=create_access_token(user.id, role_id, tenant_id, expires_delta=access_token_expires)
        ) 