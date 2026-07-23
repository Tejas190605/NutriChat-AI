import uuid
from datetime import UTC, date, datetime
from typing import TYPE_CHECKING
from uuid import uuid4

from sqlalchemy import Date, DateTime, ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.base import Base

if TYPE_CHECKING:
    from src.models.user import User


class ProgressSnapshot(Base):
    """SQLAlchemy model representing a high level status report snapshot."""

    __tablename__ = "progress_snapshots"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    date: Mapped[date] = mapped_column(Date, nullable=False, index=True)

    weight: Mapped[float | None] = mapped_column(Numeric(5, 2), nullable=True)
    body_fat_percentage: Mapped[float | None] = mapped_column(
        Numeric(4, 2), nullable=True
    )
    muscle_mass_percentage: Mapped[float | None] = mapped_column(
        Numeric(4, 2), nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC), nullable=False
    )

    user: Mapped["User"] = relationship("User")


class BodyMeasurement(Base):
    """SQLAlchemy model representing circumference measurements used to calculate Navy Body Fat."""

    __tablename__ = "body_measurements"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    date: Mapped[date] = mapped_column(Date, nullable=False, index=True)

    neck: Mapped[float | None] = mapped_column(Numeric(5, 2), nullable=True)  # in cm
    waist: Mapped[float | None] = mapped_column(Numeric(5, 2), nullable=True)  # in cm
    hip: Mapped[float | None] = mapped_column(
        Numeric(5, 2), nullable=True
    )  # in cm (critical for women)
    chest: Mapped[float | None] = mapped_column(Numeric(5, 2), nullable=True)  # in cm

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC), nullable=False
    )

    user: Mapped["User"] = relationship("User")
