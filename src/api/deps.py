from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from typing import AsyncGenerator

from infrastructure.db.session import SessionLocal
from application.use_cases.comment_use_cases import CommentUseCases
from infrastructure.repositories.sql_comment_repository import SQLCommentRepository
from application.use_cases.user_use_cases import UserUseCases
from infrastructure.repositories.sql_user_repository import SQLUserRepository


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        yield session

async def get_comment_use_cases(db: AsyncSession = Depends(get_db)) -> CommentUseCases:
    comment_repository = SQLCommentRepository(db)
    return CommentUseCases(comment_repository)

async def get_user_use_cases(db: AsyncSession = Depends(get_db)) -> UserUseCases:
    user_repository = SQLUserRepository(db)
    return UserUseCases(user_repository)
