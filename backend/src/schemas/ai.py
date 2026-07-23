from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class AIMessageCreate(BaseModel):
    """Pydantic schema representing creating an AI message."""

    role: str = Field(..., max_length=50, pattern="^(user|assistant|system|function)$")
    content: str = Field(...)
    tokens: int | None = Field(default=None, ge=0)


class AIMessageResponse(BaseModel):
    """Pydantic schema representing an AI message response."""

    id: UUID
    conversation_id: UUID
    role: str
    content: str
    tokens: int | None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class AIConversationCreate(BaseModel):
    """Pydantic schema representing creating a new conversation session."""

    title: str | None = Field(default=None, max_length=100)


class AIConversationUpdate(BaseModel):
    """Pydantic schema representing updating conversation status or title."""

    title: str | None = Field(default=None, max_length=100)
    is_active: bool | None = Field(default=None)


class AIConversationResponse(BaseModel):
    """Pydantic schema representing an active AI conversation session details."""

    id: UUID
    user_id: UUID
    title: str | None
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class PromptVersionCreate(BaseModel):
    """Pydantic schema representing creating a new prompt version configuration."""

    version: int = Field(..., gt=0)
    system_prompt: str = Field(...)
    user_prompt_template: str = Field(...)
    model_name: str = Field(..., max_length=100)
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    is_active: bool = Field(default=False)


class PromptVersionResponse(BaseModel):
    """Pydantic schema representing details of a prompt version."""

    id: UUID
    template_id: UUID
    version: int
    system_prompt: str
    user_prompt_template: str
    model_name: str
    temperature: float
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class PromptTemplateCreate(BaseModel):
    """Pydantic schema representing creating a new prompt template metadata."""

    name: str = Field(..., max_length=100)
    description: str | None = Field(default=None, max_length=255)


class PromptTemplateUpdate(BaseModel):
    """Pydantic schema representing updating a prompt template."""

    description: str | None = Field(default=None, max_length=255)


class PromptTemplateResponse(BaseModel):
    """Pydantic schema representing details of a prompt template."""

    id: UUID
    name: str
    description: str | None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class RecommendationFeedbackCreate(BaseModel):
    """Pydantic schema representing logging recommendation feedback metrics."""

    feedback_value: str = Field(
        ..., max_length=50, pattern="^(liked|disliked|dismissed)$"
    )
    comments: str | None = Field(default=None, max_length=255)


class RecommendationFeedbackResponse(BaseModel):
    """Pydantic schema representing logged recommendation feedback details."""

    id: UUID
    recommendation_id: UUID
    feedback_value: str
    comments: str | None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class RecommendationCreate(BaseModel):
    """Pydantic schema representing creating a recommendation log."""

    category: str = Field(..., max_length=50)
    content: dict[str, Any] = Field(...)


class RecommendationResponse(BaseModel):
    """Pydantic schema representing logged recommendation details."""

    id: UUID
    user_id: UUID
    category: str
    content: dict[str, Any]
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
