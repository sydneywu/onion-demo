from datetime import datetime
from dataclasses import dataclass, field
from typing import List, Optional
from uuid import UUID


@dataclass
class RoleBase:
    """Base class for Role domain model"""
    name: str
    permissions: List[UUID]


@dataclass
class Role(RoleBase):
    """Role domain model with audit fields"""
    id: Optional[UUID] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    created_by: Optional[UUID] = None
    updated_by: Optional[UUID] = None
    is_deleted: bool = False
    deleted_at: Optional[datetime] = None
    deleted_by: Optional[UUID] = None 