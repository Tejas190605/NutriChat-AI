import uuid
from datetime import UTC, datetime
from typing import TYPE_CHECKING
from uuid import uuid4

from sqlalchemy import DateTime, ForeignKey, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.base import Base

if TYPE_CHECKING:
    from src.models.user import User


class Insight(Base):
    """SQLAlchemy model representing personalized coaching advice and tips."""

    __tablename__ = "insights"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    insight_type: Mapped[str] = mapped_column(
        String(50), default="daily", nullable=False
    )  # daily/weekly/monthly

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC), nullable=False
    )

    user: Mapped["User"] = relationship("User")


class CoachingSession(Base):
    """SQLAlchemy model representing user interactive coaching sessions logs."""

    __tablename__ = "coaching_sessions"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    started_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC), nullable=False
    )
    ended_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    session_type: Mapped[str] = mapped_column(
        String(50), default="interactive", nullable=False
    )

    user: Mapped["User"] = relationship("User")


class Prediction(Base):
    """SQLAlchemy model representing weight trend forecasts and remaining calorie targets forecasts."""

    __tablename__ = "predictions"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    prediction_type: Mapped[str] = mapped_column(
        String(50), nullable=False
    )  # e.g., weight_trend, goal_date
    predicted_value: Mapped[float] = mapped_column(Numeric(8, 2), nullable=False)
    confidence_interval_low: Mapped[float | None] = mapped_column(
        Numeric(8, 2), nullable=True
    )
    confidence_interval_high: Mapped[float | None] = mapped_column(
        Numeric(8, 2), nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC), nullable=False
    )

    user: Mapped["User"] = relationship("User")
