"""analytics and coaching domain

Revision ID: 004_analytics_coaching_domain
Revises: 003_ai_persistence_domain
Create Date: 2026-07-23 01:20:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "004_analytics_coaching_domain"
down_revision: str | None = "003_ai_persistence_domain"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # 1. DailyNutritionSummary
    op.create_table(
        "daily_nutrition_summaries",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column("date", sa.Date(), nullable=False),
        sa.Column("total_calories", sa.Integer(), nullable=False),
        sa.Column("total_protein", sa.Numeric(precision=6, scale=1), nullable=False),
        sa.Column("total_carbs", sa.Numeric(precision=6, scale=1), nullable=False),
        sa.Column("total_fat", sa.Numeric(precision=6, scale=1), nullable=False),
        sa.Column("total_fiber", sa.Numeric(precision=5, scale=1), nullable=False),
        sa.Column("total_water_ml", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("idx_daily_nutrition_user"),
        "daily_nutrition_summaries",
        ["user_id"],
        unique=False,
    )
    op.create_index(
        op.f("idx_daily_nutrition_date"),
        "daily_nutrition_summaries",
        ["date"],
        unique=False,
    )

    # 2. WeeklyNutritionSummary
    op.create_table(
        "weekly_nutrition_summaries",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column("start_date", sa.Date(), nullable=False),
        sa.Column("end_date", sa.Date(), nullable=False),
        sa.Column("avg_calories", sa.Integer(), nullable=False),
        sa.Column("avg_protein", sa.Numeric(precision=6, scale=1), nullable=False),
        sa.Column("avg_carbs", sa.Numeric(precision=6, scale=1), nullable=False),
        sa.Column("avg_fat", sa.Numeric(precision=6, scale=1), nullable=False),
        sa.Column("avg_fiber", sa.Numeric(precision=5, scale=1), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("idx_weekly_nutrition_user"),
        "weekly_nutrition_summaries",
        ["user_id"],
        unique=False,
    )

    # 3. MonthlyNutritionSummary
    op.create_table(
        "monthly_nutrition_summaries",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column("year", sa.Integer(), nullable=False),
        sa.Column("month", sa.Integer(), nullable=False),
        sa.Column("avg_calories", sa.Integer(), nullable=False),
        sa.Column("avg_protein", sa.Numeric(precision=6, scale=1), nullable=False),
        sa.Column("avg_carbs", sa.Numeric(precision=6, scale=1), nullable=False),
        sa.Column("avg_fat", sa.Numeric(precision=6, scale=1), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )

    # 4. DailyActivitySummary
    op.create_table(
        "daily_activity_summaries",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column("date", sa.Date(), nullable=False),
        sa.Column("total_calories_burned", sa.Integer(), nullable=False),
        sa.Column("total_active_minutes", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )

    # 5. WeeklyActivitySummary
    op.create_table(
        "weekly_activity_summaries",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column("start_date", sa.Date(), nullable=False),
        sa.Column("end_date", sa.Date(), nullable=False),
        sa.Column("avg_calories_burned", sa.Integer(), nullable=False),
        sa.Column("total_active_minutes", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )

    # 6. GoalProgress
    op.create_table(
        "goal_progress",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column("date", sa.Date(), nullable=False),
        sa.Column("target_calories", sa.Integer(), nullable=False),
        sa.Column("consumed_calories", sa.Integer(), nullable=False),
        sa.Column("deficit_surplus", sa.Integer(), nullable=False),
        sa.Column("adherence_score", sa.Numeric(precision=5, scale=2), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )

    # 7. ProgressSnapshot
    op.create_table(
        "progress_snapshots",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column("date", sa.Date(), nullable=False),
        sa.Column("weight", sa.Numeric(precision=5, scale=2), nullable=True),
        sa.Column(
            "body_fat_percentage", sa.Numeric(precision=4, scale=2), nullable=True
        ),
        sa.Column(
            "muscle_mass_percentage", sa.Numeric(precision=4, scale=2), nullable=True
        ),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )

    # 8. BodyMeasurement
    op.create_table(
        "body_measurements",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column("date", sa.Date(), nullable=False),
        sa.Column("neck", sa.Numeric(precision=5, scale=2), nullable=True),
        sa.Column("waist", sa.Numeric(precision=5, scale=2), nullable=True),
        sa.Column("hip", sa.Numeric(precision=5, scale=2), nullable=True),
        sa.Column("chest", sa.Numeric(precision=5, scale=2), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )

    # 9. Habit
    op.create_table(
        "habits",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("description", sa.String(length=255), nullable=True),
        sa.Column("frequency", sa.String(length=20), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )

    # 10. HabitLog
    op.create_table(
        "habit_logs",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("habit_id", sa.UUID(), nullable=False),
        sa.Column("date", sa.Date(), nullable=False),
        sa.Column("is_completed", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["habit_id"], ["habits.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )

    # 11. Streak
    op.create_table(
        "streaks",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column("streak_type", sa.String(length=50), nullable=False),
        sa.Column("current_streak", sa.Integer(), nullable=False),
        sa.Column("longest_streak", sa.Integer(), nullable=False),
        sa.Column("last_updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )

    # 12. Badge
    op.create_table(
        "badges",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False, unique=True),
        sa.Column("description", sa.String(length=255), nullable=False),
        sa.Column("icon_url", sa.String(length=255), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )

    # 13. Achievement
    op.create_table(
        "achievements",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column("badge_id", sa.UUID(), nullable=False),
        sa.Column("unlocked_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["badge_id"], ["badges.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )

    # 14. Insight
    op.create_table(
        "insights",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column("title", sa.String(length=100), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("insight_type", sa.String(length=50), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )

    # 15. CoachingSession
    op.create_table(
        "coaching_sessions",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("ended_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("session_type", sa.String(length=50), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )

    # 16. Prediction
    op.create_table(
        "predictions",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column("prediction_type", sa.String(length=50), nullable=False),
        sa.Column("predicted_value", sa.Numeric(precision=8, scale=2), nullable=False),
        sa.Column(
            "confidence_interval_low", sa.Numeric(precision=8, scale=2), nullable=True
        ),
        sa.Column(
            "confidence_interval_high", sa.Numeric(precision=8, scale=2), nullable=True
        ),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )

    # 17. NotificationSchedule
    op.create_table(
        "notification_schedules",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column("time_of_day", sa.String(length=10), nullable=False),
        sa.Column("days_of_week", sa.String(length=50), nullable=False),
        sa.Column("notification_type", sa.String(length=50), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )

    # 18. Reminder
    op.create_table(
        "reminders",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column("reminder_type", sa.String(length=50), nullable=False),
        sa.Column("scheduled_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("is_sent", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("reminders")
    op.drop_table("notification_schedules")
    op.drop_table("predictions")
    op.drop_table("coaching_sessions")
    op.drop_table("insights")
    op.drop_table("achievements")
    op.drop_table("badges")
    op.drop_table("streaks")
    op.drop_table("habit_logs")
    op.drop_table("habits")
    op.drop_table("body_measurements")
    op.drop_table("progress_snapshots")
    op.drop_table("goal_progress")
    op.drop_table("weekly_activity_summaries")
    op.drop_table("daily_activity_summaries")
    op.drop_table("monthly_nutrition_summaries")
    op.drop_table("weekly_nutrition_summaries")
    op.drop_table("daily_nutrition_summaries")
