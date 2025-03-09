from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from api.deps import get_db
from application.dto.comment_dto import CommentCreateDTO, CommentUpdateDTO
from application.use_cases.comment_use_cases import CommentUseCases
from domain.models.comment import Comment
from infrastructure.repositories.sql_comment_repository import SQLCommentRepository

router = APIRouter()

@router.post("/", response_model=Comment, status_code=status.HTTP_201_CREATED)
async def create_comment(
    comment_dto: CommentCreateDTO,
    db: AsyncSession = Depends(get_db)
):
    """Create a new comment."""
    comment_repository = SQLCommentRepository(db)
    comment_service = CommentUseCases(comment_repository)
    
    # Since we don't have authentication yet, we'll use a placeholder user ID
    current_user_id = 1  # Placeholder user ID
    
    new_comment = await comment_service.create(comment_dto, current_user_id)
    return new_comment

@router.get("/{comment_id}", response_model=Comment)
async def get_comment(
    comment_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get a comment by ID."""
    comment_repository = SQLCommentRepository(db)
    comment_service = CommentUseCases(comment_repository)
    
    comment = await comment_service.get_by_id(comment_id)
    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Comment with ID {comment_id} not found"
        )
    
    return comment

@router.get("/user/{user_id}", response_model=List[Comment])
async def get_comments_by_user(
    user_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get all comments by a specific user."""
    comment_repository = SQLCommentRepository(db)
    comment_service = CommentUseCases(comment_repository)
    
    comments = await comment_service.get_by_user_id(user_id)
    return comments

@router.get("/", response_model=List[Comment])
async def get_all_comments(
    db: AsyncSession = Depends(get_db)
):
    """Get all comments."""
    comment_repository = SQLCommentRepository(db)
    comment_service = CommentUseCases(comment_repository)
    
    comments = await comment_service.get_all()
    return comments

@router.put("/{comment_id}", response_model=Comment)
async def update_comment(
    comment_id: int,
    comment_dto: CommentUpdateDTO,
    db: AsyncSession = Depends(get_db)
):
    """Update a comment."""
    comment_repository = SQLCommentRepository(db)
    comment_service = CommentUseCases(comment_repository)
    
    # Since we don't have authentication yet, we'll use a placeholder user ID
    current_user_id = 1  # Placeholder user ID
    
    updated_comment = await comment_service.update(comment_id, comment_dto, current_user_id)
    if not updated_comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Comment with ID {comment_id} not found"
        )
    
    return updated_comment

@router.delete("/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_comment(
    comment_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Delete a comment."""
    comment_repository = SQLCommentRepository(db)
    comment_service = CommentUseCases(comment_repository)
    
    # Since we don't have authentication yet, we'll use a placeholder user ID
    current_user_id = 1  # Placeholder user ID
    
    success = await comment_service.delete(comment_id, current_user_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Comment with ID {comment_id} not found"
        )
    
    return None 