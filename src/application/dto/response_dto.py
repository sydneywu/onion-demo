from typing import TypeVar, Generic, Optional, Any
from pydantic import BaseModel

T = TypeVar('T')

class ResponseDTO(BaseModel, Generic[T]):
    error_message: Optional[str] = None
    success: bool = True
    error_code: Optional[int] = None
    result: Optional[T] = None

    @classmethod
    def success_response(cls, data: T) -> 'ResponseDTO[T]':
        return cls(
            error_message=None,
            success=True,
            error_code=None,
            result=data
        )

    @classmethod
    def error_response(
        cls,
        error_message: str,
        error_code: int = 400,
        result: Optional[T] = None
    ) -> 'ResponseDTO[T]':
        return cls(
            error_message=error_message,
            success=False,
            error_code=error_code,
            result=result
        ) 