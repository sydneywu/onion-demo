// Domain Suite Generator
// This rule helps create a complete domain suite including models, repositories, DTOs, use cases, and endpoints

module.exports = {
  name: "Generate Domain Suite",
  description: "Creates a complete domain suite with all necessary files",
  run: async ({ cursor, editor }) => {
    // Get domain name from user
    const domainName = await cursor.showQuickPick({
      prompt: "Enter the domain name (e.g., Supplier, Ingredient)",
      placeHolder: "Domain name"
    });

    if (!domainName) return;

    // Convert to lowercase for file names
    const domainNameLower = domainName.toLowerCase();
    
    // Create domain model
    await editor.newFile(`src/domain/models/${domainNameLower}.py`);
    await editor.edit(`src/domain/models/${domainNameLower}.py`, {
      text: `from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class ${domainName}Base(BaseModel):
    id: Optional[int] = None
    name: str
    # Add your domain-specific fields here

class ${domainName}(${domainName}Base):
    created_at: Optional[datetime] = None
    created_by: Optional[int] = None
    updated_at: Optional[datetime] = None
    updated_by: Optional[int] = None
    deleted_at: Optional[datetime] = None
    deleted_by: Optional[int] = None
`
    });

    // Create domain repository
    await editor.newFile(`src/domain/repositories/${domainNameLower}_repository.py`);
    await editor.edit(`src/domain/repositories/${domainNameLower}_repository.py`, {
      text: `from abc import ABC, abstractmethod
from typing import Optional, List
from domain.models.${domainNameLower} import ${domainName}

class ${domainName}Repository(ABC):
    @abstractmethod
    async def add(self, ${domainNameLower}: ${domainName}) -> None:
        pass

    @abstractmethod
    async def get_by_id(self, id: int) -> Optional[${domainName}]:
        pass

    @abstractmethod
    async def get_all(self) -> List[${domainName}]:
        pass
        
    @abstractmethod
    async def update(self, ${domainNameLower}: ${domainName}) -> None:
        pass
        
    @abstractmethod
    async def delete(self, id: int) -> None:
        pass
`
    });

    // Create DTO
    await editor.newFile(`src/application/dto/${domainNameLower}_dto.py`);
    await editor.edit(`src/application/dto/${domainNameLower}_dto.py`, {
      text: `from pydantic import Field
from typing import Optional
from domain.models.${domainNameLower} import ${domainName}Base

class ${domainName}CreateDTO(${domainName}Base):
    id: Optional[int] = Field(None, exclude=True)

class ${domainName}UpdateDTO(${domainName}Base):
    pass
`
    });

    // Create use cases
    await editor.newFile(`src/application/use_cases/${domainNameLower}_use_cases.py`);
    await editor.edit(`src/application/use_cases/${domainNameLower}_use_cases.py`, {
      text: `from typing import List, Optional

from domain.models.${domainNameLower} import ${domainName}
from domain.repositories.${domainNameLower}_repository import ${domainName}Repository
from application.dto.${domainNameLower}_dto import ${domainName}CreateDTO, ${domainName}UpdateDTO


class ${domainName}UseCases:
    def __init__(self, ${domainNameLower}_repository: ${domainName}Repository):
        self.${domainNameLower}_repository = ${domainNameLower}_repository

    async def create(self, ${domainNameLower}_dto: ${domainName}CreateDTO) -> ${domainName}:
        ${domainNameLower} = ${domainName}(**${domainNameLower}_dto.dict())
        await self.${domainNameLower}_repository.add(${domainNameLower})
        return ${domainNameLower}

    async def get_by_id(self, id: int) -> Optional[${domainName}]:
        return await self.${domainNameLower}_repository.get_by_id(id)

    async def get_all(self) -> List[${domainName}]:
        ${domainNameLower}s = await self.${domainNameLower}_repository.get_all()
        return ${domainNameLower}s
        
    async def update(self, id: int, ${domainNameLower}_dto: ${domainName}UpdateDTO) -> ${domainName}:
        existing_${domainNameLower} = await self.${domainNameLower}_repository.get_by_id(id)
        if not existing_${domainNameLower}:
            raise ValueError(f"${domainName} with id {id} not found")
            
        updated_${domainNameLower} = ${domainName}(id=id, **${domainNameLower}_dto.dict())
        await self.${domainNameLower}_repository.update(updated_${domainNameLower})
        return updated_${domainNameLower}
        
    async def delete(self, id: int) -> None:
        existing_${domainNameLower} = await self.${domainNameLower}_repository.get_by_id(id)
        if not existing_${domainNameLower}:
            raise ValueError(f"${domainName} with id {id} not found")
            
        await self.${domainNameLower}_repository.delete(id)
`
    });

    // Create ORM model
    await editor.newFile(`src/infrastructure/orm/${domainNameLower}_orm_model.py`);
    await editor.edit(`src/infrastructure/orm/${domainNameLower}_orm_model.py`, {
      text: `from sqlalchemy import Column, Integer, String, DateTime, Boolean, func

from domain.models.${domainNameLower} import ${domainName}
from infrastructure.db.base_class import Base

class ${domainName}OrmModel(Base):
    __tablename__ = "${domainNameLower}s"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    # Add your domain-specific columns here
    
    created_at = Column(DateTime, nullable=False, default=func.current_timestamp())
    created_by = Column(Integer)
    updated_at = Column(DateTime, nullable=False, default=func.current_timestamp(), onupdate=func.current_timestamp())
    updated_by = Column(Integer)

    is_deleted = Column(Boolean, default=False)
    deleted_at = Column(DateTime)
    deleted_by = Column(Integer)

    @staticmethod
    def from_domain(${domainNameLower}: ${domainName}):
        """Create a ${domainName}OrmModel instance from a ${domainName} domain model."""
        return ${domainName}OrmModel(
            id=${domainNameLower}.id,
            name=${domainNameLower}.name,
            # Map other fields here
        )

    def to_domain(self) -> ${domainName}:
        """Convert this ${domainName}OrmModel instance to a ${domainName} domain model."""
        return ${domainName}(
            id=self.id, 
            name=self.name,
            # Map other fields here
            created_at=self.created_at,
            created_by=self.created_by,
            updated_at=self.updated_at,
            updated_by=self.updated_by,
            deleted_at=self.deleted_at,
            deleted_by=self.deleted_by
        )
`
    });

    // Create SQL repository implementation
    await editor.newFile(`src/infrastructure/repositories/sql_${domainNameLower}_repository.py`);
    await editor.edit(`src/infrastructure/repositories/sql_${domainNameLower}_repository.py`, {
      text: `from typing import List, Optional

from sqlalchemy.orm import Session
from sqlalchemy.future import select
from domain.models.${domainNameLower} import ${domainName}
from domain.repositories.${domainNameLower}_repository import ${domainName}Repository
from infrastructure.orm.${domainNameLower}_orm_model import ${domainName}OrmModel

class SQL${domainName}Repository(${domainName}Repository):
    def __init__(self, db_session: Session):
        self.db_session = db_session

    async def get_all(self) -> List[${domainName}]:
        result = await self.db_session.execute(
            select(${domainName}OrmModel).filter(${domainName}OrmModel.is_deleted != True)
        )
        orm_${domainNameLower}s = result.scalars().all()
        ${domainNameLower}s = [item.to_domain() for item in orm_${domainNameLower}s]
        return ${domainNameLower}s

    async def add(self, ${domainNameLower}: ${domainName}) -> None:
        orm_${domainNameLower} = ${domainName}OrmModel.from_domain(${domainNameLower})
        self.db_session.add(orm_${domainNameLower})
        await self.db_session.commit()
        
        # Update the domain model with the generated ID
        ${domainNameLower}.id = orm_${domainNameLower}.id

    async def get_by_id(self, id: int) -> Optional[${domainName}]:
        result = await self.db_session.execute(
            select(${domainName}OrmModel).filter(
                ${domainName}OrmModel.id == id,
                ${domainName}OrmModel.is_deleted != True
            )
        )
        orm_${domainNameLower} = result.scalars().first()

        if orm_${domainNameLower} is None:
            return None

        ${domainNameLower} = orm_${domainNameLower}.to_domain()
        return ${domainNameLower}
        
    async def update(self, ${domainNameLower}: ${domainName}) -> None:
        orm_${domainNameLower} = ${domainName}OrmModel.from_domain(${domainNameLower})
        await self.db_session.merge(orm_${domainNameLower})
        await self.db_session.commit()
        
    async def delete(self, id: int) -> None:
        result = await self.db_session.execute(
            select(${domainName}OrmModel).filter(${domainName}OrmModel.id == id)
        )
        orm_${domainNameLower} = result.scalars().first()
        
        if orm_${domainNameLower}:
            orm_${domainNameLower}.is_deleted = True
            orm_${domainNameLower}.deleted_at = func.current_timestamp()
            await self.db_session.commit()
`
    });

    // Create API endpoint
    await editor.newFile(`src/api/endpoints/${domainNameLower}_endpoint.py`);
    await editor.edit(`src/api/endpoints/${domainNameLower}_endpoint.py`, {
      text: `from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from application.dto.${domainNameLower}_dto import ${domainName}CreateDTO, ${domainName}UpdateDTO
from api.deps import get_db
from application.use_cases.${domainNameLower}_use_cases import ${domainName}UseCases
from domain.models.${domainNameLower} import ${domainName}
from infrastructure.repositories.sql_${domainNameLower}_repository import SQL${domainName}Repository

router = APIRouter()

@router.post("/", response_model=${domainName}, status_code=status.HTTP_201_CREATED)
async def create_${domainNameLower}(
        ${domainNameLower}_dto: ${domainName}CreateDTO,
        db: AsyncSession = Depends(get_db)
):
    ${domainNameLower}_repository = SQL${domainName}Repository(db)
    ${domainNameLower}_service = ${domainName}UseCases(${domainNameLower}_repository)
    new_${domainNameLower} = await ${domainNameLower}_service.create(${domainNameLower}_dto)
    return new_${domainNameLower}

@router.get("/", response_model=List[${domainName}])
async def get_all_${domainNameLower}s(
        db: AsyncSession = Depends(get_db)
):
    ${domainNameLower}_repository = SQL${domainName}Repository(db)
    ${domainNameLower}_service = ${domainName}UseCases(${domainNameLower}_repository)
    ${domainNameLower}s = await ${domainNameLower}_service.get_all()
    return ${domainNameLower}s
    
@router.get("/{${domainNameLower}_id}", response_model=${domainName})
async def get_${domainNameLower}(
        ${domainNameLower}_id: int,
        db: AsyncSession = Depends(get_db)
):
    ${domainNameLower}_repository = SQL${domainName}Repository(db)
    ${domainNameLower}_service = ${domainName}UseCases(${domainNameLower}_repository)
    ${domainNameLower} = await ${domainNameLower}_service.get_by_id(${domainNameLower}_id)
    
    if not ${domainNameLower}:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"${domainName} with ID {${domainNameLower}_id} not found"
        )
        
    return ${domainNameLower}
    
@router.put("/{${domainNameLower}_id}", response_model=${domainName})
async def update_${domainNameLower}(
        ${domainNameLower}_id: int,
        ${domainNameLower}_dto: ${domainName}UpdateDTO,
        db: AsyncSession = Depends(get_db)
):
    ${domainNameLower}_repository = SQL${domainName}Repository(db)
    ${domainNameLower}_service = ${domainName}UseCases(${domainNameLower}_repository)
    
    try:
        updated_${domainNameLower} = await ${domainNameLower}_service.update(${domainNameLower}_id, ${domainNameLower}_dto)
        return updated_${domainNameLower}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
        
@router.delete("/{${domainNameLower}_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_${domainNameLower}(
        ${domainNameLower}_id: int,
        db: AsyncSession = Depends(get_db)
):
    ${domainNameLower}_repository = SQL${domainName}Repository(db)
    ${domainNameLower}_service = ${domainName}UseCases(${domainNameLower}_repository)
    
    try:
        await ${domainNameLower}_service.delete(${domainNameLower}_id)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
`
    });

    // Create a helper to update the router
    await editor.newFile(`src/api/router_update_helper.js`);
    await editor.edit(`src/api/router_update_helper.js`, {
      text: `// This is a helper script to remind you to update the router.py file
// After generating a new domain suite, you need to add the new router to src/api/router.py
// Example:
/*
from fastapi import APIRouter
from api.endpoints import user_endpoint, ${domainNameLower}_endpoint  # Add your new endpoint here

api_router = APIRouter()
api_router.include_router(user_endpoint.router, prefix="/users", tags=["users"])
api_router.include_router(${domainNameLower}_endpoint.router, prefix="/${domainNameLower}s", tags=["${domainNameLower}s"])  # Add your new router here
*/

console.log("Don't forget to update src/api/router.py to include your new endpoint!");
console.log(\`Add: from api.endpoints import ${domainNameLower}_endpoint\`);
console.log(\`Add: api_router.include_router(${domainNameLower}_endpoint.router, prefix="/${domainNameLower}s", tags=["${domainNameLower}s"])\`);
`
    });

    // Show a message to the user
    await cursor.showInformationMessage(`${domainName} domain suite created successfully! Don't forget to update src/api/router.py to include your new endpoint.`);
  }
}; 