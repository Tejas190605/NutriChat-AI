import uuid
from datetime import UTC, date, datetime
from typing import TYPE_CHECKING
from uuid import uuid4

from sqlalchemy import Date, DateTime, ForeignKey, Integer, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.base import Base

if TYPE_CHECKING:
    from src.models.user import User


class DailyNutritionSummary(Base):
    """SQLAlchemy model representing aggregated daily nutrition totals."""

    __tablename__ = "daily_nutrition_summaries"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    date: Mapped[date] = mapped_column(Date, nullable=False, index=True)

    total_calories: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    total_protein: Mapped[float] = mapped_column(
        Numeric(6, 1), default=0.0, nullable=False
    )
    total_carbs: Mapped[float] = mapped_column(
        Numeric(6, 1), default=0.0, nullable=False
    )
    total_fat: Mapped[float] = mapped_column(Numeric(6, 1), default=0.0, nullable=False)
    total_fiber: Mapped[float] = mapped_column(
        Numeric(5, 1), default=0.0, nullable=False
    )
    total_water_ml: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC), nullable=False
    )

    user: Mapped["User"] = relationship("User")


class WeeklyNutritionSummary(Base):
    """SQLAlchemy model representing average macro intakes over a week."""

    __tablename__ = "weekly_nutrition_summaries"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    start_date: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    end_date: Mapped[date] = mapped_column(Date, nullable=False)

    avg_calories: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    avg_protein: Mapped[float] = mapped_column(
        Numeric(6, 1), default=0.0, nullable=False
    )
    avg_carbs: Mapped[float] = mapped_column(Numeric(6, 1), default=0.0, nullable=False)
    avg_fat: Mapped[float] = mapped_column(Numeric(6, 1), default=0.0, nullable=False)
    avg_fiber: Mapped[float] = mapped_column(Numeric(5, 1), default=0.0, nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC), nullable=False
    )

    user: Mapped["User"] = relationship("User")


class MonthlyNutritionSummary(Base):
    """SQLAlchemy model representing average macro intakes over a month."""

    __tablename__ = "monthly_nutrition_summaries"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    month: Mapped[int] = mapped_column(Integer, nullable=False)

    avg_calories: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    avg_protein: Mapped[float] = mapped_column(
        Numeric(6, 1), default=0.0, nullable=False
    )
    avg_carbs: Mapped[float] = mapped_column(Numeric(6, 1), default=0.0, nullable=False)
    avg_fat: Mapped[float] = mapped_column(Numeric(6, 1), default=0.0, nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC), nullable=False
    )

    user: Mapped["User"] = relationship("User")


class DailyActivitySummary(Base):
    """SQLAlchemy model representing aggregated activity logs calories burned."""

    __tablename__ = "daily_activity_summaries"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    date: Mapped[date] = mapped_column(Date, nullable=False, index=True)

    total_calories_burned: Mapped[int] = mapped_column(
        Integer, default=0, nullable=False
    )
    total_active_minutes: Mapped[int] = mapped_column(
        Integer, default=0, nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC), nullable=False
    )

    user: Mapped["User"] = relationship("User")


class WeeklyActivitySummary(Base):
    """SQLAlchemy model representing activity summaries averaged over a week."""

    __tablename__ = "weekly_activity_summaries"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    start_date: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    end_date: Mapped[date] = mapped_column(Date, nullable=False)

    avg_calories_burned: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    total_active_minutes: Mapped[int] = mapped_column(
        Integer, default=0, nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC), nullable=False
    )

    user: Mapped["User"] = relationship("User")


class GoalProgress(Base):
    """SQLAlchemy model tracking daily target splits adherence score metrics."""

    __tablename__ = "goal_progress"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    date: Mapped[date] = mapped_column(Date, nullable=False, index=True)

    target_calories: Mapped[int] = mapped_column(Integer, nullable=False)
    consumed_calories: Mapped[int] = mapped_column(Integer, nullable=False)
    deficit_surplus: Mapped[int] = mapped_column(Integer, nullable=False)
    adherence_score: Mapped[float] = mapped_column(
        Numeric(5, 2), default=0.0, nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC), nullable=False
    )

    user: Mapped["User"] = relationship("User")
