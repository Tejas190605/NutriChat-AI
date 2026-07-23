from __future__ import annotations

import uuid
from datetime import UTC, datetime
from uuid import uuid4

from sqlalchemy import DateTime, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from src.db.base import Base


class ConfidenceScore(Base):
    """SQLAlchemy model representing confidence scores of vision/OCR predictions, supporting soft deletes."""

    __tablename__ = "confidence_scores"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid4)
    entity_type: Mapped[str] = mapped_column(
        String(50), nullable=False, index=True
    )  # ocr, prediction, etc.
    entity_id: Mapped[uuid.UUID] = mapped_column(nullable=False, index=True)
    score: Mapped[float] = mapped_column(Numeric(5, 4), default=0.0, nullable=False)

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
