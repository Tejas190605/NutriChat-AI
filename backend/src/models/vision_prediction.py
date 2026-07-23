from __future__ import annotations

import uuid
from datetime import UTC, datetime
from typing import TYPE_CHECKING, Any
from uuid import uuid4

from sqlalchemy import JSON, DateTime, ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.base import Base

if TYPE_CHECKING:
    from src.models.food_image import FoodImage


class VisionPrediction(Base):
    """SQLAlchemy model representing individual food predictions parsed from Vision Models."""

    __tablename__ = "vision_predictions"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid4)
    food_image_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("food_images.id", ondelete="CASCADE"), nullable=False, index=True
    )
    label: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    confidence: Mapped[float] = mapped_column(
        Numeric(5, 4), default=0.0, nullable=False
    )
    box_coordinates: Mapped[dict[str, Any] | None] = mapped_column(
        JSON, nullable=True
    )  # bounding boxes coords

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

    food_image: Mapped[FoodImage] = relationship(
        "FoodImage", back_populates="predictions"
    )
