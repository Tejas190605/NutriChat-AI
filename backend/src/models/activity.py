import uuid
from datetime import UTC, datetime
from uuid import uuid4

from sqlalchemy import DateTime, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from src.db.base import Base


class ActivityLevel(Base):
    """SQLAlchemy model representing a physical activity tier and its TDEE multiplier."""

    __tablename__ = "activity_levels"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(
        String(50), unique=True, index=True, nullable=False
    )
    description: Mapped[str | None] = mapped_column(String(255), nullable=True)
    multiplier: Mapped[float] = mapped_column(
        Numeric(4, 3), nullable=False
    )  # e.g., 1.200, 1.375, 1.550
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC)
    )
