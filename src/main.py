from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncSession
from typing import AsyncGenerator
# Type-ignore for modules without stubs
from infrastructure.db.session import SessionLocal  # type: ignore
import uvicorn
from api.router import api_router  # type: ignore

app = FastAPI()
app.include_router(api_router, prefix='/api')


# Dependency
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        yield session


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8018)