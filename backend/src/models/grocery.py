from __future__ import annotations

import uuid
from datetime import UTC, datetime
from typing import TYPE_CHECKING
from uuid import uuid4

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.base import Base

if TYPE_CHECKING:
    from src.models.nutrition_fact import NutritionFact


class GroceryProduct(Base):
    """SQLAlchemy model representing a grocery item with packaging specifications."""

    __tablename__ = "grocery_products"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(String(100), index=True, nullable=False)
    brand: Mapped[str | None] = mapped_column(String(100), nullable=True)
    category: Mapped[str | None] = mapped_column(String(100), nullable=True)
    nutrition_fact_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("nutrition_facts.id", ondelete="SET NULL"), nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC), nullable=False
    )

    nutrition_fact: Mapped[NutritionFact | None] = relationship("NutritionFact")
