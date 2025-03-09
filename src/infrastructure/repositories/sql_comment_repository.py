from typing import List, Optional
from datetime import datetime

from sqlalchemy.orm import Session
from sqlalchemy.future import select
from sqlalchemy import update, delete

from domain.models.comment import Comment
from domain.repositories.comment_repository import CommentRepository
from infrastructure.orm.comment_orm_model import CommentOrmModel

class SQLCommentRepository(CommentRepository):
    def __init__(self, db_session: Session):
        self.db_session = db_session

    async def add(self, comment: Comment) -> None:
        orm_comment = CommentOrmModel.from_domain(comment)
        self.db_session.add(orm_comment)
        await self.db_session.flush()
        # Refresh to get the generated ID
        await self.db_session.refresh(orm_comment)
        # Update the domain model with the generated ID
        comment.id = orm_comment.id
        await self.db_session.commit()

    async def get_by_id(self, id: int) -> Optional[Comment]:
        result = await self.db_session.execute(
            select(CommentOrmModel).filter(CommentOrmModel.id == id, CommentOrmModel.is_deleted == False)
        )
        orm_comment = result.scalars().first()

        if orm_comment is None:
            return None

        return orm_comment.to_domain()
        
    async def get_by_user_id(self, user_id: int) -> List[Comment]:
        result = await self.db_session.execute(
            select(CommentOrmModel).filter(
                CommentOrmModel.user_id == user_id,
                CommentOrmModel.is_deleted == False
            )
        )
        orm_comments = result.scalars().all()
        return [comment.to_domain() for comment in orm_comments]

    async def get_all(self) -> List[Comment]:
        result = await self.db_session.execute(
            select(CommentOrmModel).filter(CommentOrmModel.is_deleted == False)
        )
        orm_comments = result.scalars().all()
        return [comment.to_domain() for comment in orm_comments]
        
    async def update(self, comment: Comment) -> None:
        orm_comment = CommentOrmModel.from_domain(comment)
        await self.db_session.merge(orm_comment)
        await self.db_session.commit()
        
    async def delete(self, id: int) -> None:
        # Soft delete - update is_deleted flag and deleted_at timestamp
        await self.db_session.execute(
            update(CommentOrmModel)
            .where(CommentOrmModel.id == id)
            .values(is_deleted=True, deleted_at=datetime.utcnow())
        )
        await self.db_session.commit() 