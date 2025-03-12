from typing import List, Optional
from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update

from domain.models.ingredient import Ingredient
from domain.repositories.ingredient_repository import IngredientRepository
from infrastructure.orm.ingredient_orm_model import IngredientOrmModel
from infrastructure.repositories.base_repository import SQLOperations

class SQLIngredientRepository(IngredientRepository):
    def __init__(self, db_session: AsyncSession):
        self.sql = SQLOperations[Ingredient, IngredientOrmModel](db_session)

    async def add(self, ingredient: Ingredient) -> None:
        orm_ingredient = IngredientOrmModel.from_domain(ingredient)
        await self.sql.add_with_commit(ingredient, orm_ingredient)

    async def get_by_id(self, ingredient_id: int) -> Optional[Ingredient]:
        orm_ingredient = await self.sql.get_by_id(ingredient_id, IngredientOrmModel)
        return orm_ingredient.to_domain() if orm_ingredient else None

    async def get_by_name(self, name: str) -> Optional[Ingredient]:
        result = await self.sql.db_session.execute(
            select(IngredientOrmModel)
            .filter(IngredientOrmModel.name == name)
            .filter(IngredientOrmModel.is_deleted == False)
        )
        orm_ingredient = result.scalars().first()
        return orm_ingredient.to_domain() if orm_ingredient else None

    async def get_all(self) -> List[Ingredient]:
        orm_ingredients = await self.sql.get_all(IngredientOrmModel)
        return [ingredient.to_domain() for ingredient in orm_ingredients]

    async def update(self, ingredient: Ingredient) -> None:
        orm_ingredient = IngredientOrmModel.from_domain(ingredient)
        await self.sql.update_with_commit(orm_ingredient)

    async def delete(self, ingredient_id: int, deleted_by: int) -> None:
        await self.sql.soft_delete_with_commit(ingredient_id, deleted_by, IngredientOrmModel) 