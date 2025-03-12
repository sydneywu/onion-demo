from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer
from typing import Dict

from application.dto.auth_dto import UserLoginDTO
from application.use_cases.auth_use_cases import AuthUseCases
from api.deps import get_auth_use_cases, get_current_user

router = APIRouter()
security = HTTPBearer()

@router.post("/login", response_model=dict)
async def login_json(
    form_data: UserLoginDTO,
    auth_use_cases: AuthUseCases = Depends(get_auth_use_cases)
):
    """
    JSON login endpoint for backend API.
    """
    new_login = await auth_use_cases.login_access_token(form_data)
    if not new_login.access_token:
        raise HTTPException(status_code=400, detail="Wrong User")
    return {
        "error_message": None,
        "success": True,
        "error_code": None,
        "access_token": new_login.access_token,
        "token_type": new_login.token_type
    }


@router.get("/profile", response_model=dict)
async def read_users_profile(current_user: Dict = Depends(get_current_user)):
    """
    Get current user profile information.
    """
    return {
        "error_message": None,
        "success": True,
        "error_code": None,
        "result": current_user["user"]
    } 