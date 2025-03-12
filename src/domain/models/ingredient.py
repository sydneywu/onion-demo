from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class IngredientBase(BaseModel):
    id: Optional[int] = None
    name: str
    description: str
    shelf_life: int
    unit_of_measurement: str

class Ingredient(IngredientBase):
    created_at: Optional[datetime] = None
    created_by: Optional[int] = None
    updated_at: Optional[datetime] = None
    updated_by: Optional[int] = None
    is_deleted: bool = False
    deleted_at: Optional[datetime] = None
    deleted_by: Optional[int] = None 