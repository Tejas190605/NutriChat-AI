from __future__ import annotations

import uuid
from datetime import UTC, datetime
from typing import TYPE_CHECKING
from uuid import uuid4

from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.base import Base

if TYPE_CHECKING:
    from src.models.nutrition_fact import NutritionFact


class NutritionLabel(Base):
    """SQLAlchemy model representing a parsed grocery nutrition label from OCR."""

    __tablename__ = "nutrition_labels"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid4)
    raw_text: Mapped[str | None] = mapped_column(Text, nullable=True)  # Raw OCR text
    image_url: Mapped[str | None] = mapped_column(String(512), nullable=True)
    nutrition_fact_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("nutrition_facts.id", ondelete="SET NULL"), nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC), nullable=False
    )

    nutrition_fact: Mapped[NutritionFact | None] = relationship("NutritionFact")
