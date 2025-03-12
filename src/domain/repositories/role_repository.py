from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from src.domain.models.role import Role


class RoleRepository(ABC):
    """Repository interface for Role domain model"""

    @abstractmethod
    async def add(self, role: Role) -> Role:
        """Add a new role to the repository"""
        pass

    @abstractmethod
    async def get_by_id(self, role_id: UUID) -> Optional[Role]:
        """Get a role by its ID"""
        pass

    @abstractmethod
    async def get_all(self, skip: int = 0, limit: int = 100) -> List[Role]:
        """Get all roles with pagination"""
        pass

    @abstractmethod
    async def update(self, role: Role) -> Role:
        """Update an existing role"""
        pass

    @abstractmethod
    async def delete(self, role_id: UUID, deleted_by: Optional[UUID] = None) -> bool:
        """Soft delete a role by its ID"""
        pass 