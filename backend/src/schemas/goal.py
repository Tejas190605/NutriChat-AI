from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class UserGoalCreateRequest(BaseModel):
    """Pydantic schema representing creating user macro/fitness goals."""

    goal_type: str = Field(
        ..., max_length=50, description="e.g. weight_loss, muscle_gain, maintenance"
    )
    target_weight: float | None = Field(default=None, gt=0, lt=1000)
    target_calories: int | None = Field(default=None, gt=0, lt=20000)
    target_protein: float | None = Field(default=None, gt=0, lt=1000)
    target_carbs: float | None = Field(default=None, gt=0, lt=2000)
    target_fat: float | None = Field(default=None, gt=0, lt=1000)


class UserGoalResponse(BaseModel):
    """Pydantic schema representing goal response details."""

    id: UUID
    user_id: UUID
    goal_type: str
    target_weight: float | None
    target_calories: int | None
    target_protein: float | None
    target_carbs: float | None
    target_fat: float | None
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
