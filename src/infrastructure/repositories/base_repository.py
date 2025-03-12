from typing import TypeVar, Generic, Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update
from datetime import datetime

from infrastructure.db.base_class import Base

T = TypeVar('T')
ORM = TypeVar('ORM', bound=Base)

class SQLOperations(Generic[T, ORM]):
    """
    Encapsulates common SQL operations to ensure proper async operation sequence.
    Use this class via composition in your repositories.
    """
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def add_with_commit(self, domain_entity: T, orm_entity: ORM) -> None:
        """
        Enforces the proper sequence for SQLAlchemy async operations:
        add → flush → refresh → access ID → commit
        """
        # 1. Add to session
        self.db_session.add(orm_entity)
        
        # 2. Flush to get IDs
        await self.db_session.flush()
        
        # 3. Refresh to ensure we have latest data
        await self.db_session.refresh(orm_entity)
        
        # 4. Access IDs and timestamps
        # Update the domain entity with generated values
        domain_entity.id = orm_entity.id
        domain_entity.created_at = orm_entity.created_at
        domain_entity.updated_at = orm_entity.updated_at
        
        # 5. Commit the transaction
        await self.db_session.commit()

    async def update_with_commit(self, orm_entity: ORM) -> None:
        """
        Enforces proper update sequence with commit
        """
        await self.db_session.merge(orm_entity)
        await self.db_session.commit()

    async def soft_delete_with_commit(self, entity_id: int, deleted_by: int, orm_class: type[ORM]) -> None:
        """
        Enforces proper soft delete sequence with commit
        """
        current_time = datetime.now()
        
        await self.db_session.execute(
            update(orm_class)
            .where(orm_class.id == entity_id)
            .values(
                is_deleted=True,
                deleted_at=current_time,
                deleted_by=deleted_by,
                updated_at=current_time
            )
        )
        await self.db_session.commit()

    async def get_by_id(self, entity_id: int, orm_class: type[ORM]) -> Optional[ORM]:
        """
        Common get by ID operation
        """
        result = await self.db_session.execute(
            select(orm_class)
            .filter(orm_class.id == entity_id)
            .filter(orm_class.is_deleted == False)
        )
        return result.scalars().first()

    async def get_all(self, orm_class: type[ORM]) -> List[ORM]:
        """
        Common get all operation
        """
        result = await self.db_session.execute(
            select(orm_class)
            .filter(orm_class.is_deleted == False)
        )
        return result.scalars().all() 