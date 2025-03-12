from typing import TypeVar, Generic, List
from pydantic import BaseModel

T = TypeVar('T')

class PaginatedResponseDTO(BaseModel, Generic[T]):
    total: int
    items: List[T] 