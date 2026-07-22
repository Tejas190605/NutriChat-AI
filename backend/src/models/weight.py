from __future__ import annotations

import uuid
from datetime import UTC, datetime
from typing import TYPE_CHECKING
from uuid import uuid4

from sqlalchemy import DateTime, ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.base import Base

if TYPE_CHECKING:
    from src.models.user import User


class WeightHistory(Base):
    """SQLAlchemy model tracking user weight history updates over time."""

    __tablename__ = "weight_history"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )

    weight: Mapped[float] = mapped_column(Numeric(5, 2), nullable=False)  # in kg
    logged_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC), nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC), nullable=False
    )

    user: Mapped[User] = relationship("User", back_populates="weight_history")
