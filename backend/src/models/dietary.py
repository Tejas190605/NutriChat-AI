import uuid
from datetime import UTC, datetime
from uuid import uuid4

from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, mapped_column

from src.db.base import Base


class DietaryPreference(Base):
    """SQLAlchemy model representing dietary restrictions (e.g. Vegetarian, Keto)."""

    __tablename__ = "dietary_preferences"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(
        String(100), unique=True, index=True, nullable=False
    )
    description: Mapped[str | None] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC)
    )
