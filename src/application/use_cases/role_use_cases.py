from datetime import datetime
from typing import List, Optional
from uuid import UUID

from src.application.dto.role_dto import RoleCreateDTO, RoleUpdateDTO
from src.domain.models.role import Role
from src.domain.repositories.role_repository import RoleRepository


class RoleUseCases:
    """Use cases for Role domain model"""

    def __init__(self, role_repository: RoleRepository):
        self.role_repository = role_repository

    async def create_role(self, role_create_dto: RoleCreateDTO) -> Role:
        """Create a new role"""
        now = datetime.utcnow()
        
        role = Role(
            name=role_create_dto.name,
            permissions=role_create_dto.permissions,
            created_at=now,
            updated_at=now,
            created_by=role_create_dto.created_by,
            updated_by=role_create_dto.created_by
        )
        
        return await self.role_repository.add(role)

    async def get_role_by_id(self, role_id: UUID) -> Optional[Role]:
        """Get a role by ID"""
        return await self.role_repository.get_by_id(role_id)

    async def get_all_roles(self, skip: int = 0, limit: int = 100) -> List[Role]:
        """Get all roles with pagination"""
        return await self.role_repository.get_all(skip, limit)

    async def update_role(self, role_id: UUID, role_update_dto: RoleUpdateDTO) -> Optional[Role]:
        """Update an existing role"""
        # Get the existing role
        existing_role = await self.role_repository.get_by_id(role_id)
        if not existing_role:
            return None
        
        # Update only the fields that were provided
        if role_update_dto.name is not None:
            existing_role.name = role_update_dto.name
        
        if role_update_dto.permissions is not None:
            existing_role.permissions = role_update_dto.permissions
        
        # Update audit fields
        existing_role.updated_at = datetime.utcnow()
        existing_role.updated_by = role_update_dto.updated_by
        
        # Save the updated role
        return await self.role_repository.update(existing_role)

    async def delete_role(self, role_id: UUID, deleted_by: Optional[UUID] = None) -> bool:
        """Delete a role by ID"""
        return await self.role_repository.delete(role_id, deleted_by) 