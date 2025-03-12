from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from api.deps import get_db, get_comment_use_cases, get_current_user
from application.dto.comment_dto import CommentCreateDTO, CommentUpdateDTO
from application.use_cases.comment_use_cases import CommentUseCases
from domain.models.comment import Comment
from application.dto.response_dto import ResponseDTO
from application.dto.pagination_dto import PaginatedResponseDTO
from typing import Dict

router = APIRouter()

@router.post("/", response_model=ResponseDTO[Comment], status_code=status.HTTP_201_CREATED)
async def create_comment(
    comment_dto: CommentCreateDTO,
    comment_service: CommentUseCases = Depends(get_comment_use_cases),
    current_user: Dict = Depends(get_current_user)
) -> ResponseDTO[Comment]:
    """Create a new comment."""
    try:
        new_comment = await comment_service.create(comment_dto, current_user["user"].id)
        return ResponseDTO.success_response(new_comment)
    except HTTPException as e:
        return ResponseDTO.error_response(
            error_message=e.detail,
            error_code=e.status_code
        )

@router.get("/{comment_id}", response_model=ResponseDTO[Comment])
async def get_comment(
    comment_id: int,
    comment_service: CommentUseCases = Depends(get_comment_use_cases)
) -> ResponseDTO[Comment]:
    """Get a comment by ID."""
    try:
        comment = await comment_service.get_by_id(comment_id)
        if not comment:
            return ResponseDTO.error_response(
                error_message=f"Comment with ID {comment_id} not found",
                error_code=status.HTTP_404_NOT_FOUND
            )
        return ResponseDTO.success_response(comment)
    except HTTPException as e:
        return ResponseDTO.error_response(
            error_message=e.detail,
            error_code=e.status_code
        )

@router.get("/user/{user_id}", response_model=ResponseDTO[PaginatedResponseDTO[Comment]])
async def get_comments_by_user(
    user_id: int,
    comment_service: CommentUseCases = Depends(get_comment_use_cases)
) -> ResponseDTO[PaginatedResponseDTO[Comment]]:
    """Get all comments by a specific user."""
    try:
        comments = await comment_service.get_by_user_id(user_id)
        paginated_response = PaginatedResponseDTO[Comment](
            total=len(comments),
            items=comments
        )
        return ResponseDTO.success_response(paginated_response)
    except HTTPException as e:
        return ResponseDTO.error_response(
            error_message=e.detail,
            error_code=e.status_code
        )

@router.get("/", response_model=ResponseDTO[PaginatedResponseDTO[Comment]])
async def get_all_comments(
    comment_service: CommentUseCases = Depends(get_comment_use_cases)
) -> ResponseDTO[PaginatedResponseDTO[Comment]]:
    """Get all comments."""
    try:
        comments = await comment_service.get_all()
        paginated_response = PaginatedResponseDTO[Comment](
            total=len(comments),
            items=comments
        )
        return ResponseDTO.success_response(paginated_response)
    except HTTPException as e:
        return ResponseDTO.error_response(
            error_message=e.detail,
            error_code=e.status_code
        )

@router.put("/{comment_id}", response_model=ResponseDTO[Comment])
async def update_comment(
    comment_id: int,
    comment_dto: CommentUpdateDTO,
    comment_service: CommentUseCases = Depends(get_comment_use_cases),
    current_user: Dict = Depends(get_current_user)
) -> ResponseDTO[Comment]:
    """Update a comment."""
    try:
        updated_comment = await comment_service.update(comment_id, comment_dto, current_user["user"].id)
        if not updated_comment:
            return ResponseDTO.error_response(
                error_message=f"Comment with ID {comment_id} not found",
                error_code=status.HTTP_404_NOT_FOUND
            )
        return ResponseDTO.success_response(updated_comment)
    except HTTPException as e:
        return ResponseDTO.error_response(
            error_message=e.detail,
            error_code=e.status_code
        )

@router.delete("/{comment_id}", response_model=ResponseDTO[None])
async def delete_comment(
    comment_id: int,
    comment_service: CommentUseCases = Depends(get_comment_use_cases),
    current_user: Dict = Depends(get_current_user)
) -> ResponseDTO[None]:
    """Delete a comment."""
    try:
        success = await comment_service.delete(comment_id, current_user["user"].id)
        if not success:
            return ResponseDTO.error_response(
                error_message=f"Comment with ID {comment_id} not found",
                error_code=status.HTTP_404_NOT_FOUND
            )
        return ResponseDTO.success_response(None)
    except HTTPException as e:
        return ResponseDTO.error_response(
            error_message=e.detail,
            error_code=e.status_code
        ) 