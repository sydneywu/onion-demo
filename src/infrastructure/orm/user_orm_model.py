from sqlalchemy import Column, Integer, String, DateTime, Boolean, func

from domain.models.user import User
from infrastructure.db.base_class import Base

class UserOrmModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    created_at = Column(DateTime, nullable=False, default=func.current_timestamp())
    created_by = Column(Integer)
    updated_at = Column(DateTime, nullable=False, default=func.current_timestamp(), onupdate=func.current_timestamp())
    updated_by = Column(Integer)

    is_deleted = Column(Boolean)
    deleted_at = Column(DateTime)
    deleted_by = Column(Integer)

    @staticmethod
    def from_domain(user: User):
        """Create a UserOrmModel instance from a User domain model."""
        return UserOrmModel(
            id=user.id,
            username=user.username,
            email=user.email,
            hashed_password=user.hashed_password
        )

    def to_domain(self) -> User:
        """Convert this UserOrmModel instance to a User domain model."""
        return User(id=self.id, username=self.username,
                    email=self.email, hashed_password=self.hashed_password)