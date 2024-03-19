from sqlalchemy import Column, Integer, String

from domain.models.user import User
from infrastructure.db.base_class import Base

class UserOrmModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)

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