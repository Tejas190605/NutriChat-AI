from __future__ import annotations

import uuid
from datetime import UTC, datetime
from typing import TYPE_CHECKING
from uuid import uuid4

from sqlalchemy import DateTime, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.base import Base

if TYPE_CHECKING:
    from src.models.food import Food
    from src.models.meal import Meal


class MealItem(Base):
    """SQLAlchemy model representing a specific food portion consumed within a parent Meal."""

    __tablename__ = "meal_items"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid4)
    meal_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("meals.id", ondelete="CASCADE"), nullable=False, index=True
    )
    food_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("foods.id", ondelete="SET NULL"), nullable=True
    )

    food_name: Mapped[str] = mapped_column(
        String(100), nullable=False
    )  # Custom or matched food name
    quantity: Mapped[float] = mapped_column(
        Numeric(5, 2), default=1.00, nullable=False
    )  # e.g., 2.00
    unit: Mapped[str] = mapped_column(
        String(20), default="serving", nullable=False
    )  # e.g., "slice", "bowl"
    weight_grams: Mapped[float | None] = mapped_column(
        Numeric(6, 2), nullable=True
    )  # calculated absolute weight in g

    calories: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    protein: Mapped[float] = mapped_column(Numeric(5, 2), default=0.00, nullable=False)
    carbs: Mapped[float] = mapped_column(Numeric(5, 2), default=0.00, nullable=False)
    fat: Mapped[float] = mapped_column(Numeric(5, 2), default=0.00, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC), nullable=False
    )

    meal: Mapped[Meal] = relationship("Meal", back_populates="items")
    food: Mapped[Food | None] = relationship("Food")
