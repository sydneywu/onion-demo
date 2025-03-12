from datetime import datetime
from typing import List, Optional
from uuid import UUID, uuid4

from sqlalchemy import Column, String, Boolean, DateTime, func
from sqlalchemy.dialects.postgresql import UUID as PgUUID, JSONB
from sqlalchemy.ext.declarative import declarative_base

from src.domain.models.role import Role

Base = declarative_base()


class RoleORM(Base):
    """SQLAlchemy ORM model for Role"""
    __tablename__ = "roles"

    id = Column(PgUUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String, nullable=False)
    permissions = Column(JSONB, nullable=False, default=list)
    
    # Audit fields
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    created_by = Column(PgUUID(as_uuid=True), nullable=True)
    updated_by = Column(PgUUID(as_uuid=True), nullable=True)
    is_deleted = Column(Boolean, default=False, nullable=False)
    deleted_at = Column(DateTime, nullable=True)
    deleted_by = Column(PgUUID(as_uuid=True), nullable=True)

    @classmethod
    def from_domain(cls, role: Role) -> "RoleORM":
        """Convert domain model to ORM model"""
        return cls(
            id=role.id,
            name=role.name,
            permissions=role.permissions,
            created_at=role.created_at,
            updated_at=role.updated_at,
            created_by=role.created_by,
            updated_by=role.updated_by,
            is_deleted=role.is_deleted,
            deleted_at=role.deleted_at,
            deleted_by=role.deleted_by
        )

    def to_domain(self) -> Role:
        """Convert ORM model to domain model"""
        return Role(
            id=self.id,
            name=self.name,
            permissions=self.permissions,
            created_at=self.created_at,
            updated_at=self.updated_at,
            created_by=self.created_by,
            updated_by=self.updated_by,
            is_deleted=self.is_deleted,
            deleted_at=self.deleted_at,
            deleted_by=self.deleted_by
        ) 