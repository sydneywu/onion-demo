from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncSession
from typing import AsyncGenerator
# Type-ignore for modules without stubs
from infrastructure.db.session import SessionLocal  # type: ignore
import uvicorn
from api.router import api_router  # type: ignore
from config import settings

app = FastAPI(
    docs_url="/shaker_docs",
    redoc_url=None,  # Disable ReDoc
    swagger_ui_parameters={"persistAuthorization": True}
)
app.include_router(api_router, prefix='/api')


# Dependency
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        yield session


if __name__ == "__main__":
    uvicorn.run(
        app, 
        host=settings.API_HOST, 
        port=settings.API_PORT
    )