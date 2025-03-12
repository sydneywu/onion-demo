from pydantic import BaseModel, Field
from typing import Optional
from domain.models.ingredient import IngredientBase

class IngredientCreateDTO(BaseModel):
    name: str
    description: str
    shelf_life: int
    unit_of_measurement: str

class IngredientUpdateDTO(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    shelf_life: Optional[int] = None
    unit_of_measurement: Optional[str] = None 