import pytest
from unittest.mock import AsyncMock, MagicMock
from datetime import datetime
from typing import List, Optional

from application.use_cases.user_use_cases import UserUseCases
from application.dto.user_dto import UserRegistrationDTO
from domain.models.user import User
from domain.repositories.user_repository import UserRepository


class MockUserRepository(UserRepository):
    """Mock implementation of UserRepository for testing"""
    
    def __init__(self):
        self.users = {}
        self.next_id = 1
        self.users_by_email = {}
        
    async def add(self, user: User) -> None:
        user.id = self.next_id
        user.created_at = datetime.utcnow()
        user.updated_at = datetime.utcnow()
        self.users[self.next_id] = user
        self.users_by_email[user.email] = user
        self.next_id += 1
        
    async def get_by_email(self, email: str) -> Optional[User]:
        return self.users_by_email.get(email)
        
    async def get_all(self) -> List[User]:
        return list(self.users.values())


@pytest.mark.asyncio
async def test_register_user_success():
    # Arrange
    user_repository = MockUserRepository()
    user_use_cases = UserUseCases(user_repository)
    
    user_dto = UserRegistrationDTO(
        username="testuser",
        email="test@example.com",
        password="password123"
    )
    
    # Act
    result = await user_use_cases.register(user_dto)
    
    # Assert
    assert result.id == 1
    assert result.username == "testuser"
    assert result.email == "test@example.com"
    assert result.hashed_password == "password123_hashed"  # Check password hashing
    assert result.created_at is not None


@pytest.mark.asyncio
async def test_get_all_users():
    # Arrange
    user_repository = MockUserRepository()
    user_use_cases = UserUseCases(user_repository)
    
    # Add multiple users
    user1 = User(username="user1", email="user1@example.com", hashed_password="hashed1")
    user2 = User(username="user2", email="user2@example.com", hashed_password="hashed2")
    
    await user_repository.add(user1)
    await user_repository.add(user2)
    
    # Act
    all_users = await user_use_cases.get_all()
    
    # Assert
    assert len(all_users) == 2
    assert any(user.username == "user1" for user in all_users)
    assert any(user.username == "user2" for user in all_users)


@pytest.mark.asyncio
async def test_user_model_has_is_deleted_field():
    """Test to ensure the User model has the is_deleted field as per CursorRules"""
    # Arrange
    user = User(
        username="testuser",
        email="test@example.com",
        hashed_password="hashed_password"
    )
    
    # Assert
    assert hasattr(user, "is_deleted") is True, "User model should have is_deleted field"
    assert user.is_deleted is False, "is_deleted should default to False" 