from typing import List, Optional
from fastapi import HTTPException, status

from domain.models.ingredient import Ingredient
from domain.repositories.ingredient_repository import IngredientRepository
from application.dto.ingredient_dto import IngredientCreateDTO, IngredientUpdateDTO


class IngredientUseCases:
    def __init__(self, ingredient_repository: IngredientRepository):
        self.ingredient_repository = ingredient_repository

    async def create(self, ingredient_dto: IngredientCreateDTO, created_by: Optional[int] = None) -> Ingredient:
        # Check if ingredient with the same name already exists
        existing_ingredient = await self.ingredient_repository.get_by_name(ingredient_dto.name)
        if existing_ingredient:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Ingredient with name '{ingredient_dto.name}' already exists"
            )

        # Create new ingredient
        ingredient = Ingredient(
            name=ingredient_dto.name,
            description=ingredient_dto.description,
            shelf_life=ingredient_dto.shelf_life,
            unit_of_measurement=ingredient_dto.unit_of_measurement,
            created_by=created_by
        )
        await self.ingredient_repository.add(ingredient)
        return ingredient

    async def get_by_id(self, ingredient_id: int) -> Ingredient:
        ingredient = await self.ingredient_repository.get_by_id(ingredient_id)
        if not ingredient:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Ingredient with ID {ingredient_id} not found"
            )
        return ingredient

    async def get_all(self) -> List[Ingredient]:
        ingredients = await self.ingredient_repository.get_all()
        return ingredients

    async def update(self, ingredient_id: int, ingredient_dto: IngredientUpdateDTO, updated_by: Optional[int] = None) -> Ingredient:
        # Check if ingredient exists
        existing_ingredient = await self.ingredient_repository.get_by_id(ingredient_id)
        if not existing_ingredient:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Ingredient with ID {ingredient_id} not found"
            )

        # Check if name is being updated and if it already exists
        if ingredient_dto.name and ingredient_dto.name != existing_ingredient.name:
            name_exists = await self.ingredient_repository.get_by_name(ingredient_dto.name)
            if name_exists:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"Ingredient with name '{ingredient_dto.name}' already exists"
                )

        # Update fields if provided
        if ingredient_dto.name is not None:
            existing_ingredient.name = ingredient_dto.name
        if ingredient_dto.description is not None:
            existing_ingredient.description = ingredient_dto.description
        if ingredient_dto.shelf_life is not None:
            existing_ingredient.shelf_life = ingredient_dto.shelf_life
        if ingredient_dto.unit_of_measurement is not None:
            existing_ingredient.unit_of_measurement = ingredient_dto.unit_of_measurement

        existing_ingredient.updated_by = updated_by
        await self.ingredient_repository.update(existing_ingredient)
        return existing_ingredient

    async def delete(self, ingredient_id: int, deleted_by: Optional[int] = None) -> None:
        # Check if ingredient exists
        existing_ingredient = await self.ingredient_repository.get_by_id(ingredient_id)
        if not existing_ingredient:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Ingredient with ID {ingredient_id} not found"
            )

        await self.ingredient_repository.delete(ingredient_id, deleted_by) 