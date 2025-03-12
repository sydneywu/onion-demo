from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.ext.asyncio import AsyncSession
from typing import AsyncGenerator
# Type-ignore for modules without stubs
from infrastructure.db.session import SessionLocal  # type: ignore
import uvicorn
from api.router import api_router  # type: ignore
from config import settings
from application.dto.response_dto import ResponseDTO

app = FastAPI(
    docs_url="/shaker_docs",
    redoc_url=None,  # Disable ReDoc
    swagger_ui_parameters={"persistAuthorization": True}
)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=ResponseDTO.error_response(
            error_message=str(exc),
            error_code=status.HTTP_422_UNPROCESSABLE_ENTITY
        ).model_dump()
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=ResponseDTO.error_response(
            error_message=str(exc),
            error_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        ).model_dump()
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