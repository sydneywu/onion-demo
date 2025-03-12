from typing import List, Optional, Dict

from fastapi import APIRouter, Depends, HTTPException, status, Query, Path
from sqlalchemy.ext.asyncio import AsyncSession

from domain.models.ingredient import Ingredient
from application.dto.ingredient_dto import IngredientCreateDTO, IngredientUpdateDTO
from application.use_cases.ingredient_use_cases import IngredientUseCases
from application.dto.response_dto import ResponseDTO
from application.dto.pagination_dto import PaginatedResponseDTO
from api.deps import get_db, get_current_user, get_ingredient_use_cases

router = APIRouter()

@router.post("/", response_model=ResponseDTO[Ingredient], status_code=status.HTTP_201_CREATED)
async def create_ingredient(
    ingredient_dto: IngredientCreateDTO,
    ingredient_use_cases: IngredientUseCases = Depends(get_ingredient_use_cases),
    current_user: Dict = Depends(get_current_user)
) -> ResponseDTO[Ingredient]:
    """
    Create a new ingredient.
    """
    result = await ingredient_use_cases.create(ingredient_dto, created_by=current_user["user"].id)
    return ResponseDTO.success_response(result)

@router.get("/", response_model=ResponseDTO[PaginatedResponseDTO[Ingredient]])
async def get_all_ingredients(
    ingredient_use_cases: IngredientUseCases = Depends(get_ingredient_use_cases)
) -> ResponseDTO[PaginatedResponseDTO[Ingredient]]:
    """
    Get all ingredients.
    """
    ingredients = await ingredient_use_cases.get_all()
    paginated_response = PaginatedResponseDTO[Ingredient](
        total=len(ingredients),
        items=ingredients
    )
    return ResponseDTO.success_response(paginated_response)

@router.get("/{ingredient_id}", response_model=ResponseDTO[Ingredient])
async def get_ingredient(
    ingredient_id: int = Path(..., gt=0),
    ingredient_use_cases: IngredientUseCases = Depends(get_ingredient_use_cases)
) -> ResponseDTO[Ingredient]:
    """
    Get an ingredient by ID.
    """
    try:
        result = await ingredient_use_cases.get_by_id(ingredient_id)
        return ResponseDTO.success_response(result)
    except HTTPException as e:
        return ResponseDTO.error_response(
            error_message=e.detail,
            error_code=e.status_code
        )

@router.put("/{ingredient_id}", response_model=ResponseDTO[Ingredient])
async def update_ingredient(
    ingredient_dto: IngredientUpdateDTO,
    ingredient_id: int = Path(..., gt=0),
    ingredient_use_cases: IngredientUseCases = Depends(get_ingredient_use_cases),
    current_user: Dict = Depends(get_current_user)
) -> ResponseDTO[Ingredient]:
    """
    Update an ingredient.
    """
    try:
        result = await ingredient_use_cases.update(ingredient_id, ingredient_dto, updated_by=current_user["user"].id)
        return ResponseDTO.success_response(result)
    except HTTPException as e:
        return ResponseDTO.error_response(
            error_message=e.detail,
            error_code=e.status_code
        )

@router.delete("/{ingredient_id}", response_model=ResponseDTO[None])
async def delete_ingredient(
    ingredient_id: int = Path(..., gt=0),
    ingredient_use_cases: IngredientUseCases = Depends(get_ingredient_use_cases),
    current_user: Dict = Depends(get_current_user)
) -> ResponseDTO[None]:
    """
    Delete an ingredient.
    """
    try:
        await ingredient_use_cases.delete(ingredient_id, deleted_by=current_user["user"].id)
        return ResponseDTO.success_response(None)
    except HTTPException as e:
        return ResponseDTO.error_response(
            error_message=e.detail,
            error_code=e.status_code
        ) 