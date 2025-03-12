from typing import List, Optional, Dict

from fastapi import APIRouter, Depends, HTTPException, status, Query, Path
from sqlalchemy.ext.asyncio import AsyncSession

from domain.models.ingredient import Ingredient
from application.dto.ingredient_dto import IngredientCreateDTO, IngredientUpdateDTO
from application.use_cases.ingredient_use_cases import IngredientUseCases
from api.deps import get_db, get_current_user, get_ingredient_use_cases

router = APIRouter()

@router.post("/", response_model=Ingredient, status_code=status.HTTP_201_CREATED)
async def create_ingredient(
    ingredient_dto: IngredientCreateDTO,
    ingredient_use_cases: IngredientUseCases = Depends(get_ingredient_use_cases),
    current_user: Dict = Depends(get_current_user)
) -> Ingredient:
    """
    Create a new ingredient.
    """
    return await ingredient_use_cases.create(ingredient_dto, created_by=current_user["user"].id)

@router.get("/", response_model=List[Ingredient])
async def get_all_ingredients(
    ingredient_use_cases: IngredientUseCases = Depends(get_ingredient_use_cases)
) -> List[Ingredient]:
    """
    Get all ingredients.
    """
    return await ingredient_use_cases.get_all()

@router.get("/{ingredient_id}", response_model=Ingredient)
async def get_ingredient(
    ingredient_id: int = Path(..., gt=0),
    ingredient_use_cases: IngredientUseCases = Depends(get_ingredient_use_cases)
) -> Ingredient:
    """
    Get an ingredient by ID.
    """
    return await ingredient_use_cases.get_by_id(ingredient_id)

@router.put("/{ingredient_id}", response_model=Ingredient)
async def update_ingredient(
    ingredient_dto: IngredientUpdateDTO,
    ingredient_id: int = Path(..., gt=0),
    ingredient_use_cases: IngredientUseCases = Depends(get_ingredient_use_cases),
    current_user: Dict = Depends(get_current_user)
) -> Ingredient:
    """
    Update an ingredient.
    """
    return await ingredient_use_cases.update(ingredient_id, ingredient_dto, updated_by=current_user["user"].id)

@router.delete("/{ingredient_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_ingredient(
    ingredient_id: int = Path(..., gt=0),
    ingredient_use_cases: IngredientUseCases = Depends(get_ingredient_use_cases),
    current_user: Dict = Depends(get_current_user)
) -> None:
    """
    Delete an ingredient.
    """
    await ingredient_use_cases.delete(ingredient_id, deleted_by=current_user["user"].id)
    return None 