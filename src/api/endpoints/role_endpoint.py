from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse

from src.application.dto.role_dto import RoleCreateDTO, RoleUpdateDTO, RoleResponseDTO
from src.application.use_cases.role_use_cases import RoleUseCases
from src.api.deps import get_role_use_cases

router = APIRouter(prefix="/roles", tags=["roles"])


@router.post("", response_model=RoleResponseDTO, status_code=status.HTTP_201_CREATED)
async def create_role(
    role_data: RoleCreateDTO,
    role_use_cases: RoleUseCases = Depends(get_role_use_cases)
):
    """Create a new role"""
    try:
        role = await role_use_cases.create_role(role_data)
        return RoleResponseDTO(
            id=role.id,
            name=role.name,
            permissions=role.permissions,
            created_at=role.created_at.isoformat() if role.created_at else None,
            updated_at=role.updated_at.isoformat() if role.updated_at else None
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create role: {str(e)}"
        )


@router.get("/{role_id}", response_model=RoleResponseDTO)
async def get_role(
    role_id: UUID,
    role_use_cases: RoleUseCases = Depends(get_role_use_cases)
):
    """Get a role by ID"""
    role = await role_use_cases.get_role_by_id(role_id)
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Role with ID {role_id} not found"
        )
    
    return RoleResponseDTO(
        id=role.id,
        name=role.name,
        permissions=role.permissions,
        created_at=role.created_at.isoformat() if role.created_at else None,
        updated_at=role.updated_at.isoformat() if role.updated_at else None
    )


@router.get("", response_model=List[RoleResponseDTO])
async def get_all_roles(
    skip: int = 0,
    limit: int = 100,
    role_use_cases: RoleUseCases = Depends(get_role_use_cases)
):
    """Get all roles with pagination"""
    roles = await role_use_cases.get_all_roles(skip, limit)
    
    return [
        RoleResponseDTO(
            id=role.id,
            name=role.name,
            permissions=role.permissions,
            created_at=role.created_at.isoformat() if role.created_at else None,
            updated_at=role.updated_at.isoformat() if role.updated_at else None
        )
        for role in roles
    ]


@router.put("/{role_id}", response_model=RoleResponseDTO)
async def update_role(
    role_id: UUID,
    role_data: RoleUpdateDTO,
    role_use_cases: RoleUseCases = Depends(get_role_use_cases)
):
    """Update an existing role"""
    updated_role = await role_use_cases.update_role(role_id, role_data)
    
    if not updated_role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Role with ID {role_id} not found"
        )
    
    return RoleResponseDTO(
        id=updated_role.id,
        name=updated_role.name,
        permissions=updated_role.permissions,
        created_at=updated_role.created_at.isoformat() if updated_role.created_at else None,
        updated_at=updated_role.updated_at.isoformat() if updated_role.updated_at else None
    )


@router.delete("/{role_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_role(
    role_id: UUID,
    deleted_by: Optional[UUID] = None,
    role_use_cases: RoleUseCases = Depends(get_role_use_cases)
):
    """Delete a role by ID"""
    success = await role_use_cases.delete_role(role_id, deleted_by)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Role with ID {role_id} not found"
        )
    
    return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content=None) 