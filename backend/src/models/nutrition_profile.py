from __future__ import annotations

import uuid
from datetime import UTC, datetime
from typing import TYPE_CHECKING
from uuid import uuid4

from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.base import Base

if TYPE_CHECKING:
    from src.models.food import Food
    from src.models.nutrition_fact import NutritionFact


class NutritionProfile(Base):
    """SQLAlchemy model linking Food or Ingredient entities to their corresponding NutritionFact."""

    __tablename__ = "nutrition_profiles"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid4)
    food_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("foods.id", ondelete="CASCADE"), unique=True, nullable=True
    )
    ingredient_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("ingredients.id", ondelete="CASCADE"), unique=True, nullable=True
    )
    nutrition_fact_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("nutrition_facts.id", ondelete="CASCADE"), nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC), nullable=False
    )

    food: Mapped[Food | None] = relationship("Food", back_populates="nutrition_profile")
    nutrition_fact: Mapped[NutritionFact] = relationship("NutritionFact")
