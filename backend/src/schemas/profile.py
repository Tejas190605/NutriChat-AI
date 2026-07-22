from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class UserProfileUpdateRequest(BaseModel):
    """Pydantic schema representing user profile updates."""

    first_name: str | None = Field(default=None, max_length=100)
    last_name: str | None = Field(default=None, max_length=100)
    phone_number: str | None = Field(default=None, max_length=30)
    gender: str | None = Field(default=None, max_length=20)
    date_of_birth: date | None = Field(default=None)
    height: float | None = Field(default=None, gt=0, lt=300)  # in cm
    weight: float | None = Field(default=None, gt=0, lt=1000)  # in kg


class UserProfileResponse(BaseModel):
    """Pydantic schema representing profile response models."""

    id: UUID
    user_id: UUID
    first_name: str | None
    last_name: str | None
    phone_number: str | None
    gender: str | None
    date_of_birth: date | None
    height: float | None
    weight: float | None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
