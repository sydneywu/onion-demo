from sqlalchemy import Column, Integer, String, DateTime, Boolean, func
from datetime import datetime

from domain.models.ingredient import Ingredient
from infrastructure.db.base_class import Base

class IngredientOrmModel(Base):
    __tablename__ = "ingredients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    description = Column(String, nullable=False)
    shelf_life = Column(Integer, nullable=False)
    unit_of_measurement = Column(String, nullable=False)
    
    # Audit fields
    created_at = Column(DateTime, nullable=False, default=func.current_timestamp())
    created_by = Column(Integer)
    updated_at = Column(DateTime, nullable=False, default=func.current_timestamp(), onupdate=func.current_timestamp())
    updated_by = Column(Integer)
    
    # Soft delete fields
    is_deleted = Column(Boolean, default=False)
    deleted_at = Column(DateTime)
    deleted_by = Column(Integer)

    @staticmethod
    def from_domain(ingredient: Ingredient) -> "IngredientOrmModel":
        """Create an IngredientOrmModel instance from an Ingredient domain model."""
        return IngredientOrmModel(
            id=ingredient.id,
            name=ingredient.name,
            description=ingredient.description,
            shelf_life=ingredient.shelf_life,
            unit_of_measurement=ingredient.unit_of_measurement,
            created_at=ingredient.created_at,
            created_by=ingredient.created_by,
            updated_at=ingredient.updated_at,
            updated_by=ingredient.updated_by,
            is_deleted=ingredient.is_deleted,
            deleted_at=ingredient.deleted_at,
            deleted_by=ingredient.deleted_by
        )

    def to_domain(self) -> Ingredient:
        """Convert this IngredientOrmModel instance to an Ingredient domain model."""
        return Ingredient(
            id=self.id,
            name=self.name,
            description=self.description,
            shelf_life=self.shelf_life,
            unit_of_measurement=self.unit_of_measurement,
            created_at=self.created_at,
            created_by=self.created_by,
            updated_at=self.updated_at,
            updated_by=self.updated_by,
            is_deleted=self.is_deleted,
            deleted_at=self.deleted_at,
            deleted_by=self.deleted_by
        ) 