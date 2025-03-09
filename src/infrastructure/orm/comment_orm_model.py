from sqlalchemy import Column, Integer, String, DateTime, Boolean, func, Text, ForeignKey
from sqlalchemy.orm import relationship

from domain.models.comment import Comment
from infrastructure.db.base_class import Base

class CommentOrmModel(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(Text)
    user_id = Column(Integer, ForeignKey("users.id"))
    
    created_at = Column(DateTime, nullable=False, default=func.current_timestamp())
    created_by = Column(Integer)
    updated_at = Column(DateTime, nullable=False, default=func.current_timestamp(), onupdate=func.current_timestamp())
    updated_by = Column(Integer)

    is_deleted = Column(Boolean, default=False)
    deleted_at = Column(DateTime)
    deleted_by = Column(Integer)
    
    # Relationship with User model
    user = relationship("UserOrmModel", back_populates="comments")

    @staticmethod
    def from_domain(comment: Comment):
        """Create a CommentOrmModel instance from a Comment domain model."""
        return CommentOrmModel(
            id=comment.id,
            name=comment.name,
            description=comment.description,
            user_id=comment.user_id,
            created_at=comment.created_at,
            created_by=comment.created_by,
            updated_at=comment.updated_at,
            updated_by=comment.updated_by,
            deleted_at=comment.deleted_at,
            deleted_by=comment.deleted_by
        )

    def to_domain(self) -> Comment:
        """Convert this CommentOrmModel instance to a Comment domain model."""
        return Comment(
            id=self.id,
            name=self.name,
            description=self.description,
            user_id=self.user_id,
            created_at=self.created_at,
            created_by=self.created_by,
            updated_at=self.updated_at,
            updated_by=self.updated_by,
            deleted_at=self.deleted_at,
            deleted_by=self.deleted_by
        ) 