from __future__ import annotations

import uuid
from datetime import UTC, datetime
from typing import TYPE_CHECKING
from uuid import uuid4

from sqlalchemy import Column, DateTime, ForeignKey, String, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.base import Base

# Association table for food-ingredients mapping
food_ingredients = Table(
    "food_ingredients",
    Base.metadata,
    Column("food_id", ForeignKey("foods.id", ondelete="CASCADE"), primary_key=True),
    Column(
        "ingredient_id",
        ForeignKey("ingredients.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column("quantity", String(50), nullable=True),  # e.g., "50g", "1 tbsp"
)

if TYPE_CHECKING:
    from src.models.category import FoodCategory
    from src.models.ingredient import Ingredient
    from src.models.nutrition_profile import NutritionProfile


class Food(Base):
    """SQLAlchemy model representing a specific food item (e.g. Chicken Biryani, Masala Dosa)."""

    __tablename__ = "foods"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(
        String(100), unique=True, index=True, nullable=False
    )
    description: Mapped[str | None] = mapped_column(String(255), nullable=True)
    category_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("food_categories.id", ondelete="SET NULL"), nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC), nullable=False
    )

    category: Mapped[FoodCategory | None] = relationship(
        "FoodCategory", back_populates="foods"
    )
    ingredients: Mapped[list[Ingredient]] = relationship(
        "Ingredient",
        secondary=food_ingredients,
        back_populates="foods",
    )
    nutrition_profile: Mapped[NutritionProfile | None] = relationship(
        "NutritionProfile",
        back_populates="food",
        cascade="all, delete-orphan",
        uselist=False,
    )
