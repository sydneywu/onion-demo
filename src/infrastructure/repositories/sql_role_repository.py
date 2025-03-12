from datetime import datetime
from typing import List, Optional
from uuid import UUID

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.models.role import Role
from src.domain.repositories.role_repository import RoleRepository
from src.infrastructure.orm.role_orm_model import RoleORM


class SQLRoleRepository(RoleRepository):
    """SQL implementation of the Role repository"""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, role: Role) -> Role:
        """Add a new role to the repository"""
        role_orm = RoleORM.from_domain(role)
        self.session.add(role_orm)
        await self.session.flush()
        await self.session.refresh(role_orm)
        return role_orm.to_domain()

    async def get_by_id(self, role_id: UUID) -> Optional[Role]:
        """Get a role by its ID"""
        query = select(RoleORM).where(
            RoleORM.id == role_id,
            RoleORM.is_deleted == False
        )
        result = await self.session.execute(query)
        role_orm = result.scalars().first()
        
        if not role_orm:
            return None
            
        return role_orm.to_domain()

    async def get_all(self, skip: int = 0, limit: int = 100) -> List[Role]:
        """Get all roles with pagination"""
        query = select(RoleORM).where(
            RoleORM.is_deleted == False
        ).offset(skip).limit(limit)
        
        result = await self.session.execute(query)
        role_orms = result.scalars().all()
        
        return [role_orm.to_domain() for role_orm in role_orms]

    async def update(self, role: Role) -> Role:
        """Update an existing role"""
        role_orm = RoleORM.from_domain(role)
        
        # Merge the updated role with the session
        merged_role = await self.session.merge(role_orm)
        await self.session.flush()
        await self.session.refresh(merged_role)
        
        return merged_role.to_domain()

    async def delete(self, role_id: UUID, deleted_by: Optional[UUID] = None) -> bool:
        """Soft delete a role by its ID"""
        now = datetime.utcnow()
        
        query = update(RoleORM).where(
            RoleORM.id == role_id,
            RoleORM.is_deleted == False
        ).values(
            is_deleted=True,
            deleted_at=now,
            deleted_by=deleted_by
        )
        
        result = await self.session.execute(query)
        await self.session.flush()
        
        return result.rowcount > 0 