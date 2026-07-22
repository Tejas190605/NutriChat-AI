from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr

from src.schemas.profile import UserProfileResponse


class UserResponse(BaseModel):
    """Pydantic schema representing basic user response metadata."""

    id: UUID
    email: EmailStr
    is_active: bool
    is_superuser: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class UserDetailResponse(UserResponse):
    """Pydantic schema representing user profile detailing relationships."""

    profile: UserProfileResponse | None = None

    model_config = ConfigDict(from_attributes=True)
