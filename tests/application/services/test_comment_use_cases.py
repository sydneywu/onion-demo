import pytest
from unittest.mock import AsyncMock, MagicMock
from datetime import datetime
from typing import List, Optional

from application.use_cases.comment_use_cases import CommentUseCases
from application.dto.comment_dto import CommentCreateDTO, CommentUpdateDTO
from domain.models.comment import Comment
from domain.repositories.comment_repository import CommentRepository


class MockCommentRepository(CommentRepository):
    """Mock implementation of CommentRepository for testing"""
    
    def __init__(self):
        self.comments = {}
        self.next_id = 1
        
    async def add(self, comment: Comment) -> None:
        comment.id = self.next_id
        comment.created_at = datetime.utcnow()
        comment.updated_at = datetime.utcnow()
        self.comments[self.next_id] = comment
        self.next_id += 1
        
    async def get_by_id(self, id: int) -> Optional[Comment]:
        return self.comments.get(id)
        
    async def get_by_user_id(self, user_id: int) -> List[Comment]:
        return [comment for comment in self.comments.values() if comment.user_id == user_id]
        
    async def get_all(self) -> List[Comment]:
        return list(self.comments.values())
        
    async def update(self, comment: Comment) -> None:
        if comment.id in self.comments:
            comment.updated_at = datetime.utcnow()
            self.comments[comment.id] = comment
            
    async def delete(self, id: int) -> None:
        if id in self.comments:
            self.comments[id].deleted_at = datetime.utcnow()


@pytest.mark.asyncio
async def test_create_comment_success():
    # Arrange
    comment_repository = MockCommentRepository()
    comment_use_cases = CommentUseCases(comment_repository)
    
    comment_dto = CommentCreateDTO(
        name="Test Comment",
        description="This is a test comment",
        user_id=1
    )
    user_id = 1
    
    # Act
    result = await comment_use_cases.create(comment_dto, user_id)
    
    # Assert
    assert result.id == 1
    assert result.name == "Test Comment"
    assert result.description == "This is a test comment"
    assert result.user_id == 1
    assert result.created_by == user_id
    assert result.created_at is not None


@pytest.mark.asyncio
async def test_get_comment_by_id_success():
    # Arrange
    comment_repository = MockCommentRepository()
    comment_use_cases = CommentUseCases(comment_repository)
    
    # Add a comment first
    comment = Comment(
        name="Test Comment",
        description="This is a test comment",
        user_id=1,
        created_by=1
    )
    await comment_repository.add(comment)
    
    # Act
    result = await comment_use_cases.get_by_id(1)
    
    # Assert
    assert result is not None
    assert result.id == 1
    assert result.name == "Test Comment"
    assert result.description == "This is a test comment"


@pytest.mark.asyncio
async def test_get_comment_by_id_not_found():
    # Arrange
    comment_repository = MockCommentRepository()
    comment_use_cases = CommentUseCases(comment_repository)
    
    # Act
    result = await comment_use_cases.get_by_id(999)  # Non-existent ID
    
    # Assert
    assert result is None


@pytest.mark.asyncio
async def test_get_comments_by_user_id():
    # Arrange
    comment_repository = MockCommentRepository()
    comment_use_cases = CommentUseCases(comment_repository)
    
    # Add comments for different users
    comment1 = Comment(name="User 1 Comment 1", description="Description 1", user_id=1, created_by=1)
    comment2 = Comment(name="User 1 Comment 2", description="Description 2", user_id=1, created_by=1)
    comment3 = Comment(name="User 2 Comment", description="Description 3", user_id=2, created_by=2)
    
    await comment_repository.add(comment1)
    await comment_repository.add(comment2)
    await comment_repository.add(comment3)
    
    # Act
    user1_comments = await comment_use_cases.get_by_user_id(1)
    user2_comments = await comment_use_cases.get_by_user_id(2)
    
    # Assert
    assert len(user1_comments) == 2
    assert len(user2_comments) == 1
    assert all(comment.user_id == 1 for comment in user1_comments)
    assert all(comment.user_id == 2 for comment in user2_comments)


@pytest.mark.asyncio
async def test_get_all_comments():
    # Arrange
    comment_repository = MockCommentRepository()
    comment_use_cases = CommentUseCases(comment_repository)
    
    # Add multiple comments
    comment1 = Comment(name="Comment 1", description="Description 1", user_id=1, created_by=1)
    comment2 = Comment(name="Comment 2", description="Description 2", user_id=2, created_by=2)
    
    await comment_repository.add(comment1)
    await comment_repository.add(comment2)
    
    # Act
    all_comments = await comment_use_cases.get_all()
    
    # Assert
    assert len(all_comments) == 2


@pytest.mark.asyncio
async def test_update_comment_success():
    # Arrange
    comment_repository = MockCommentRepository()
    comment_use_cases = CommentUseCases(comment_repository)
    
    # Add a comment first
    comment = Comment(
        name="Original Name",
        description="Original Description",
        user_id=1,
        created_by=1
    )
    await comment_repository.add(comment)
    
    # Create update DTO
    update_dto = CommentUpdateDTO(
        name="Updated Name",
        description="Updated Description",
        user_id=1
    )
    
    # Act
    updated_comment = await comment_use_cases.update(1, update_dto, 2)  # User ID 2 is updating
    
    # Assert
    assert updated_comment is not None
    assert updated_comment.name == "Updated Name"
    assert updated_comment.description == "Updated Description"
    assert updated_comment.updated_by == 2  # Check that updater ID is set


@pytest.mark.asyncio
async def test_update_comment_not_found():
    # Arrange
    comment_repository = MockCommentRepository()
    comment_use_cases = CommentUseCases(comment_repository)
    
    update_dto = CommentUpdateDTO(
        name="Updated Name",
        description="Updated Description",
        user_id=1
    )
    
    # Act
    result = await comment_use_cases.update(999, update_dto, 1)  # Non-existent ID
    
    # Assert
    assert result is None


@pytest.mark.asyncio
async def test_delete_comment_success():
    # Arrange
    comment_repository = MockCommentRepository()
    comment_use_cases = CommentUseCases(comment_repository)
    
    # Add a comment first
    comment = Comment(
        name="Comment to Delete",
        description="This comment will be deleted",
        user_id=1,
        created_by=1
    )
    await comment_repository.add(comment)
    
    # Act
    result = await comment_use_cases.delete(1, 2)  # User ID 2 is deleting
    
    # Assert
    assert result is True
    deleted_comment = await comment_repository.get_by_id(1)
    assert deleted_comment.deleted_by == 2  # Check that deleter ID is set
    assert deleted_comment.deleted_at is not None  # Check that deleted_at is set


@pytest.mark.asyncio
async def test_delete_comment_not_found():
    # Arrange
    comment_repository = MockCommentRepository()
    comment_use_cases = CommentUseCases(comment_repository)
    
    # Act
    result = await comment_use_cases.delete(999, 1)  # Non-existent ID
    
    # Assert
    assert result is False 