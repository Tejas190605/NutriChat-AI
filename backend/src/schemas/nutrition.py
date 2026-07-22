from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class NutritionFactResponse(BaseModel):
    """Pydantic schema representing nutrition facts values."""

    id: UUID
    calories: int
    protein: float
    carbs: float
    fat: float
    fiber: float
    sugar: float
    sodium: float
    saturated_fat: float
    serving_size: float
    serving_unit: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class FoodCategoryResponse(BaseModel):
    """Pydantic schema representing a food category."""

    id: UUID
    name: str
    description: str | None = None

    model_config = ConfigDict(from_attributes=True)


class FoodResponse(BaseModel):
    """Pydantic schema representing a food item."""

    id: UUID
    name: str
    description: str | None = None
    category_id: UUID | None = None
    nutrition_fact: NutritionFactResponse | None = None

    model_config = ConfigDict(from_attributes=True)


class BarcodeProductResponse(BaseModel):
    """Pydantic schema representing barcode lookup products."""

    id: UUID
    barcode: str
    product_name: str
    brand: str | None = None
    nutrition_fact: NutritionFactResponse | None = None

    model_config = ConfigDict(from_attributes=True)


class FavoriteFoodResponse(BaseModel):
    """Pydantic schema representing user favorite foods."""

    id: UUID
    user_id: UUID
    food: FoodResponse

    model_config = ConfigDict(from_attributes=True)


class RecentFoodResponse(BaseModel):
    """Pydantic schema representing user recent foods logs."""

    id: UUID
    user_id: UUID
    food: FoodResponse
    last_used_at: datetime

    model_config = ConfigDict(from_attributes=True)
