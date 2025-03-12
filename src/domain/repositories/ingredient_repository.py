from abc import ABC, abstractmethod
from typing import Optional, List
from domain.models.ingredient import Ingredient

class IngredientRepository(ABC):
    @abstractmethod
    async def add(self, ingredient: Ingredient) -> None:
        pass

    @abstractmethod
    async def get_by_id(self, ingredient_id: int) -> Optional[Ingredient]:
        pass

    @abstractmethod
    async def get_by_name(self, name: str) -> Optional[Ingredient]:
        pass

    @abstractmethod
    async def get_all(self) -> List[Ingredient]:
        pass

    @abstractmethod
    async def update(self, ingredient: Ingredient) -> None:
        pass

    @abstractmethod
    async def delete(self, ingredient_id: int, deleted_by: int) -> None:
        pass 