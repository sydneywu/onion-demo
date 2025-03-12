from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import AsyncGenerator, Dict, Optional
from jose import jwt, JWTError, ExpiredSignatureError
from pydantic import ValidationError

from infrastructure.db.session import SessionLocal
from application.use_cases.comment_use_cases import CommentUseCases
from infrastructure.repositories.sql_comment_repository import SQLCommentRepository
from application.use_cases.user_use_cases import UserUseCases
from infrastructure.repositories.sql_user_repository import SQLUserRepository
from application.use_cases.auth_use_cases import AuthUseCases
from infrastructure.repositories.sql_auth_repository import SQLAuthRepository
from domain.models.auth import TokenPayload
from utils.security import SECRET_KEY, ALGORITHM


security = HTTPBearer()


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        yield session


async def get_comment_use_cases(db: AsyncSession = Depends(get_db)) -> CommentUseCases:
    comment_repository = SQLCommentRepository(db)
    return CommentUseCases(comment_repository)


async def get_user_use_cases(db: AsyncSession = Depends(get_db)) -> UserUseCases:
    user_repository = SQLUserRepository(db)
    return UserUseCases(user_repository)


async def get_auth_use_cases(db: AsyncSession = Depends(get_db)) -> AuthUseCases:
    auth_repository = SQLAuthRepository(db)
    return AuthUseCases(auth_repository)


async def get_current_user(
    db: AsyncSession = Depends(get_db), 
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> Dict:
    """
    Get the current authenticated user.
    """
    try:
        token = credentials.credentials
        payload = jwt.decode(
            token, SECRET_KEY, algorithms=[ALGORITHM]
        )
        token_data = TokenPayload(**payload)
        
        if token_data.sub is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
            )
            
        # Get user by ID
        user_repository = SQLUserRepository(db)
        user_service = UserUseCases(user_repository)
        user = await user_repository.get_by_id(int(token_data.sub))
        
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
            )
            
        # For now, we'll return a simple dict with user info
        # In a real application, you would also include role and tenant info
        return {
            "user": user,
            "role_id": token_data.role_id,
            "tenant_id": token_data.tenant_id
        }
            
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired"
        )
    except (JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials"
        )
