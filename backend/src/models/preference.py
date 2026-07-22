from __future__ import annotations

import uuid
from datetime import UTC, datetime, time
from typing import TYPE_CHECKING
from uuid import uuid4

from sqlalchemy import Boolean, DateTime, ForeignKey, String, Time
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.base import Base

if TYPE_CHECKING:
    from src.models.user import User


class UserPreference(Base):
    """SQLAlchemy model representing custom user application settings."""

    __tablename__ = "user_preferences"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False
    )

    language: Mapped[str] = mapped_column(String(10), default="en", nullable=False)
    units_system: Mapped[str] = mapped_column(
        String(20), default="metric", nullable=False
    )  # metric or imperial

    daily_reminder_enabled: Mapped[bool] = mapped_column(
        Boolean, default=True, nullable=False
    )
    daily_reminder_time: Mapped[time] = mapped_column(
        Time, default=time(9, 0, 0), nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
        nullable=False,
    )

    user: Mapped[User] = relationship("User", back_populates="preference")
