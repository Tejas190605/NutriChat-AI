from __future__ import annotations

import uuid
from datetime import UTC, datetime
from typing import TYPE_CHECKING, Any
from uuid import uuid4

from sqlalchemy import JSON, DateTime, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.base import Base

if TYPE_CHECKING:
    from src.models.prompt import PromptVersion
    from src.models.usage import TokenUsage
    from src.models.user import User


class AIRequest(Base):
    """SQLAlchemy model representing an outgoing call request to an AI Model, supporting soft deletes."""

    __tablename__ = "ai_requests"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid4)
    user_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True
    )
    prompt_version_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("prompt_versions.id", ondelete="SET NULL"), nullable=True, index=True
    )
    request_payload: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
        nullable=False,
    )
    deleted_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True, index=True
    )

    user: Mapped[User | None] = relationship("User")
    prompt_version: Mapped[PromptVersion | None] = relationship(
        "PromptVersion", back_populates="ai_requests"
    )
    ai_response: Mapped[AIResponse | None] = relationship(
        "AIResponse",
        back_populates="ai_request",
        cascade="all, delete-orphan",
        uselist=False,
    )
    token_usages: Mapped[list[TokenUsage]] = relationship(
        "TokenUsage",
        back_populates="ai_request",
        cascade="all, delete-orphan",
    )


class AIResponse(Base):
    """SQLAlchemy model representing the incoming response matching an AIRequest, supporting soft deletes."""

    __tablename__ = "ai_responses"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid4)
    request_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("ai_requests.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
        index=True,
    )
    response_payload: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)
    latency_ms: Mapped[int] = mapped_column(Integer, nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
        nullable=False,
    )
    deleted_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True, index=True
    )

    ai_request: Mapped[AIRequest] = relationship(
        "AIRequest", back_populates="ai_response"
    )
