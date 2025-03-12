from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer
from typing import Dict

from application.dto.auth_dto import UserLoginDTO
from application.use_cases.auth_use_cases import AuthUseCases
from api.deps import get_auth_use_cases, get_current_user
from application.dto.response_dto import ResponseDTO
from domain.models.auth import Token

router = APIRouter()
security = HTTPBearer()

@router.post("/login", response_model=ResponseDTO[Token])
async def login_json(
    form_data: UserLoginDTO,
    auth_use_cases: AuthUseCases = Depends(get_auth_use_cases)
) -> ResponseDTO[Token]:
    """
    JSON login endpoint for backend API.
    """
    try:
        new_login = await auth_use_cases.login_access_token(form_data)
        return ResponseDTO.success_response(new_login)
    except HTTPException as e:
        return ResponseDTO.error_response(
            error_message=e.detail,
            error_code=e.status_code
        )

@router.get("/profile", response_model=ResponseDTO[Dict])
async def read_users_profile(
    current_user: Dict = Depends(get_current_user)
) -> ResponseDTO[Dict]:
    """
    Get current user profile information.
    """
    return ResponseDTO.success_response(current_user["user"]) 