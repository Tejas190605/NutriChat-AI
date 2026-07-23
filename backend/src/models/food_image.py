from __future__ import annotations

import uuid
from datetime import UTC, datetime
from typing import TYPE_CHECKING
from uuid import uuid4

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.base import Base

if TYPE_CHECKING:
    from src.models.ocr_result import OCRResult
    from src.models.user import User
    from src.models.vision_prediction import VisionPrediction


class FoodImage(Base):
    """SQLAlchemy model representing food photo uploads, supporting soft deletes."""

    __tablename__ = "food_images"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    image_url: Mapped[str] = mapped_column(String(512), nullable=False)
    status: Mapped[str] = mapped_column(
        String(50), default="uploaded", nullable=False, index=True
    )  # uploaded, processing, parsed, failed

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

    user: Mapped[User] = relationship("User")
    ocr_results: Mapped[list[OCRResult]] = relationship(
        "OCRResult",
        back_populates="food_image",
        cascade="all, delete-orphan",
    )
    predictions: Mapped[list[VisionPrediction]] = relationship(
        "VisionPrediction",
        back_populates="food_image",
        cascade="all, delete-orphan",
    )
