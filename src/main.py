from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncSession
from infrastructure.db.session import SessionLocal
import uvicorn
from api.router import api_router

app = FastAPI()
app.include_router(api_router, prefix='/api')


# Dependency
async def get_db() -> AsyncSession:
    async with SessionLocal() as session:
        yield session


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8018)