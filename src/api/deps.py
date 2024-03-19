from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.db.session import SessionLocal


async def get_db() -> AsyncSession:
    async with SessionLocal() as session:
        yield session
