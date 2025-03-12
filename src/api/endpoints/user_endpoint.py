from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from application.dto.user_dto import UserRegistrationDTO
from api.deps import get_db, get_user_use_cases
from application.use_cases.user_use_cases import UserUseCases
from domain.models.user import User
from application.dto.response_dto import ResponseDTO
from application.dto.pagination_dto import PaginatedResponseDTO

router = APIRouter()

@router.post("/", response_model=ResponseDTO[User])
async def register(
    user_dto: UserRegistrationDTO,
    user_service: UserUseCases = Depends(get_user_use_cases)
) -> ResponseDTO[User]:
    """Register a new user."""
    try:
        new_user = await user_service.register(user_dto)
        return ResponseDTO.success_response(new_user)
    except HTTPException as e:
        return ResponseDTO.error_response(
            error_message=e.detail,
            error_code=e.status_code
        )

@router.get("/", response_model=ResponseDTO[PaginatedResponseDTO[User]])
async def get_all_users(
    user_service: UserUseCases = Depends(get_user_use_cases)
) -> ResponseDTO[PaginatedResponseDTO[User]]:
    """Get all users."""
    users = await user_service.get_all()
    paginated_response = PaginatedResponseDTO[User](
        total=len(users),
        items=users
    )
    return ResponseDTO.success_response(paginated_response)