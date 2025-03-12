from typing import List, Optional
from uuid import UUID
from pydantic import BaseModel, Field


class RoleCreateDTO(BaseModel):
    """Data Transfer Object for creating a role"""
    name: str = Field(..., description="The name of the role")
    permissions: List[UUID] = Field(default_factory=list, description="List of permission IDs associated with this role")
    created_by: Optional[UUID] = Field(None, description="ID of the user creating this role")


class RoleUpdateDTO(BaseModel):
    """Data Transfer Object for updating a role"""
    name: Optional[str] = Field(None, description="The name of the role")
    permissions: Optional[List[UUID]] = Field(None, description="List of permission IDs associated with this role")
    updated_by: Optional[UUID] = Field(None, description="ID of the user updating this role")


class RoleResponseDTO(BaseModel):
    """Data Transfer Object for role responses"""
    id: UUID
    name: str
    permissions: List[UUID]
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    
    class Config:
        orm_mode = True 