from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class MealItemCreate(BaseModel):
    """Pydantic schema representing creating an item inside a Meal log."""

    food_name: str = Field(..., max_length=100)
    quantity: float = Field(..., gt=0)
    unit: str = Field(default="serving", max_length=20)
    weight_grams: float | None = Field(default=None, gt=0)
    calories: int = Field(default=0, ge=0)
    protein: float = Field(default=0.0, ge=0.0)
    carbs: float = Field(default=0.0, ge=0.0)
    fat: float = Field(default=0.0, ge=0.0)


class MealItemResponse(BaseModel):
    """Pydantic schema representing details of a logged meal item."""

    id: UUID
    meal_id: UUID
    food_id: UUID | None = None
    food_name: str
    quantity: float
    unit: str
    weight_grams: float | None = None
    calories: int
    protein: float
    carbs: float
    fat: float

    model_config = ConfigDict(from_attributes=True)


class MealCreateRequest(BaseModel):
    """Pydantic schema representing logging a new meal."""

    name: str = Field(
        ..., max_length=100, description="e.g. Breakfast, Lunch, Dinner, Snack"
    )
    items: list[MealItemCreate] = Field(..., min_length=1)
    image_url: str | None = Field(default=None, max_length=512)
    logged_at: datetime | None = Field(default=None)


class MealUpdateRequest(BaseModel):
    """Pydantic schema representing updating a logged meal."""

    name: str | None = Field(default=None, max_length=100)
    items: list[MealItemCreate] | None = None
    image_url: str | None = Field(default=None, max_length=512)


class MealResponse(BaseModel):
    """Pydantic schema representing details of a logged meal."""

    id: UUID
    user_id: UUID
    name: str
    image_url: str | None
    logged_at: datetime
    created_at: datetime
    items: list[MealItemResponse]

    model_config = ConfigDict(from_attributes=True)


class DailySummaryResponse(BaseModel):
    """Pydantic schema representing aggregated macro progress vs target metrics."""

    date: str
    target_calories: int | None = None
    consumed_calories: int
    target_protein: float | None = None
    consumed_protein: float
    target_carbs: float | None = None
    consumed_carbs: float
    target_fat: float | None = None
    consumed_fat: float


class DailyMacros(BaseModel):
    """Calorie and macronutrient variables."""

    calories: int
    protein: float
    carbs: float
    fat: float


class WeeklySummaryResponse(BaseModel):
    """Pydantic schema representing weekly macro averages."""

    start_date: str
    end_date: str
    daily_average: DailyMacros
    days: dict[str, DailyMacros]
