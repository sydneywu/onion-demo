from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from application.dto.user_dto import UserRegistrationDTO
from api.deps import get_db, get_user_use_cases
from application.use_cases.user_use_cases import UserUseCases
from domain.models.user import User
from dataclasses import asdict

router = APIRouter()

@router.post("/", response_model=User)
async def register(
        user_dto: UserRegistrationDTO,
        user_service: UserUseCases = Depends(get_user_use_cases)
) -> User:
    new_user = await user_service.register(user_dto)
    return new_user

@router.get("/", response_model=List[User])
async def get_all_users(
        user_service: UserUseCases = Depends(get_user_use_cases)
) -> List[User]:
    users = await user_service.get_all()
    return users