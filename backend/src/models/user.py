from __future__ import annotations

import uuid
from datetime import UTC, datetime
from typing import TYPE_CHECKING
from uuid import uuid4

from sqlalchemy import Boolean, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.base import Base
from src.models.associations import user_allergies, user_dietary_preferences

if TYPE_CHECKING:
    from src.models.allergy import Allergy
    from src.models.audit import AuditLog
    from src.models.dietary import DietaryPreference
    from src.models.goal import UserGoal
    from src.models.preference import UserPreference
    from src.models.profile import UserProfile
    from src.models.session import UserSession
    from src.models.token import RefreshToken
    from src.models.weight import WeightHistory


class User(Base):
    """SQLAlchemy model representing dashboard admin users and system clients."""

    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid4)
    email: Mapped[str] = mapped_column(
        String(255), unique=True, index=True, nullable=False
    )
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    # Timestamps & Soft delete
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
        DateTime(timezone=True), nullable=True
    )

    # 1-to-1 Relationships
    profile: Mapped[UserProfile] = relationship(
        "UserProfile",
        back_populates="user",
        cascade="all, delete-orphan",
        uselist=False,
    )
    preference: Mapped[UserPreference] = relationship(
        "UserPreference",
        back_populates="user",
        cascade="all, delete-orphan",
        uselist=False,
    )

    # 1-to-Many Relationships
    goals: Mapped[list[UserGoal]] = relationship(
        "UserGoal",
        back_populates="user",
        cascade="all, delete-orphan",
        order_by="UserGoal.created_at.desc()",
    )
    weight_history: Mapped[list[WeightHistory]] = relationship(
        "WeightHistory",
        back_populates="user",
        cascade="all, delete-orphan",
        order_by="WeightHistory.logged_at.desc()",
    )
    sessions: Mapped[list[UserSession]] = relationship(
        "UserSession",
        back_populates="user",
        cascade="all, delete-orphan",
    )
    refresh_tokens: Mapped[list[RefreshToken]] = relationship(
        "RefreshToken",
        back_populates="user",
        cascade="all, delete-orphan",
    )
    audit_logs: Mapped[list[AuditLog]] = relationship(
        "AuditLog",
        back_populates="user",
        cascade="all, delete-orphan",
    )

    # Many-to-Many Relationships
    allergies: Mapped[list[Allergy]] = relationship(
        "Allergy",
        secondary=user_allergies,
    )
    dietary_preferences: Mapped[list[DietaryPreference]] = relationship(
        "DietaryPreference",
        secondary=user_dietary_preferences,
    )
