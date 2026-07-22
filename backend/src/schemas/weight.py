from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class WeightLogCreateRequest(BaseModel):
    """Pydantic schema representing logging a new weight entry."""

    weight: float = Field(..., gt=0, lt=1000)


class WeightLogResponse(BaseModel):
    """Pydantic schema representing weight log details."""

    id: UUID
    user_id: UUID
    weight: float
    logged_at: datetime
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
