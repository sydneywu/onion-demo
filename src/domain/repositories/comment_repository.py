from abc import ABC, abstractmethod
from typing import Optional, List
from domain.models.comment import Comment

class CommentRepository(ABC):
    @abstractmethod
    async def add(self, comment: Comment) -> None:
        pass

    @abstractmethod
    async def get_by_id(self, id: int) -> Optional[Comment]:
        pass
        
    @abstractmethod
    async def get_by_user_id(self, user_id: int) -> List[Comment]:
        pass

    @abstractmethod
    async def get_all(self) -> List[Comment]:
        pass
        
    @abstractmethod
    async def update(self, comment: Comment) -> None:
        pass
        
    @abstractmethod
    async def delete(self, id: int) -> None:
        pass 