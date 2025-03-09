from typing import List, Optional

from domain.models.comment import Comment
from domain.repositories.comment_repository import CommentRepository
from application.dto.comment_dto import CommentCreateDTO, CommentUpdateDTO


class CommentUseCases:
    def __init__(self, comment_repository: CommentRepository):
        self.comment_repository = comment_repository

    async def create(self, comment_dto: CommentCreateDTO, user_id: int) -> Comment:
        comment = Comment(
            name=comment_dto.name,
            description=comment_dto.description,
            user_id=comment_dto.user_id,
            created_by=user_id
        )
        await self.comment_repository.add(comment)
        return comment

    async def get_by_id(self, id: int) -> Optional[Comment]:
        return await self.comment_repository.get_by_id(id)
        
    async def get_by_user_id(self, user_id: int) -> List[Comment]:
        return await self.comment_repository.get_by_user_id(user_id)

    async def get_all(self) -> List[Comment]:
        return await self.comment_repository.get_all()
        
    async def update(self, id: int, comment_dto: CommentUpdateDTO, user_id: int) -> Optional[Comment]:
        existing_comment = await self.comment_repository.get_by_id(id)
        if not existing_comment:
            return None
            
        # Update only provided fields
        if comment_dto.name is not None:
            existing_comment.name = comment_dto.name
        if comment_dto.description is not None:
            existing_comment.description = comment_dto.description
        if comment_dto.user_id is not None:
            existing_comment.user_id = comment_dto.user_id
            
        existing_comment.updated_by = user_id
        
        await self.comment_repository.update(existing_comment)
        return existing_comment
        
    async def delete(self, id: int, user_id: int) -> bool:
        existing_comment = await self.comment_repository.get_by_id(id)
        if not existing_comment:
            return False
            
        # Soft delete by updating the deleted_by field
        existing_comment.deleted_by = user_id
        await self.comment_repository.update(existing_comment)
        
        # Hard delete
        await self.comment_repository.delete(id)
        return True 