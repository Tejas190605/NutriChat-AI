from __future__ import annotations

import uuid
from datetime import UTC, datetime
from uuid import uuid4

from sqlalchemy import DateTime, Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from src.db.base import Base


class NutritionFact(Base):
    """SQLAlchemy model representing the exact nutrient values per serving."""

    __tablename__ = "nutrition_facts"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid4)
    calories: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    protein: Mapped[float] = mapped_column(
        Numeric(5, 2), default=0.00, nullable=False
    )  # in grams
    carbs: Mapped[float] = mapped_column(
        Numeric(5, 2), default=0.00, nullable=False
    )  # in grams
    fat: Mapped[float] = mapped_column(
        Numeric(5, 2), default=0.00, nullable=False
    )  # in grams
    fiber: Mapped[float] = mapped_column(
        Numeric(5, 2), default=0.00, nullable=False
    )  # in grams
    sugar: Mapped[float] = mapped_column(
        Numeric(5, 2), default=0.00, nullable=False
    )  # in grams
    sodium: Mapped[float] = mapped_column(
        Numeric(7, 2), default=0.00, nullable=False
    )  # in mg
    saturated_fat: Mapped[float] = mapped_column(
        Numeric(5, 2), default=0.00, nullable=False
    )  # in grams
    serving_size: Mapped[float] = mapped_column(
        Numeric(5, 2), default=100.00, nullable=False
    )  # e.g., 100.00
    serving_unit: Mapped[str] = mapped_column(
        String(20), default="g", nullable=False
    )  # e.g., "g", "ml"
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC), nullable=False
    )
