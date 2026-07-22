from __future__ import annotations

import uuid
from datetime import UTC, datetime
from typing import TYPE_CHECKING
from uuid import uuid4

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.base import Base

if TYPE_CHECKING:
    from src.models.user import User


class UserGoal(Base):
    """SQLAlchemy model representing user fitness and macro nutrient goals."""

    __tablename__ = "user_goals"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )

    goal_type: Mapped[str] = mapped_column(
        String(50), nullable=False
    )  # e.g., weight_loss, muscle_gain
    target_weight: Mapped[float | None] = mapped_column(
        Numeric(5, 2), nullable=True
    )  # in kg

    target_calories: Mapped[int | None] = mapped_column(Integer, nullable=True)
    target_protein: Mapped[float | None] = mapped_column(
        Numeric(5, 2), nullable=True
    )  # in grams
    target_carbs: Mapped[float | None] = mapped_column(
        Numeric(5, 2), nullable=True
    )  # in grams
    target_fat: Mapped[float | None] = mapped_column(
        Numeric(5, 2), nullable=True
    )  # in grams

    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
        nullable=False,
    )

    user: Mapped[User] = relationship("User", back_populates="goals")
