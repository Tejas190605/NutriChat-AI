"""Initial user domain schema

Revision ID: 001_initial_user_domain
Revises:
Create Date: 2026-07-22 23:55:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "001_initial_user_domain"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # 1. Create allergies table
    op.create_table(
        "allergies",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("description", sa.String(length=255), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("idx_allergies_name"), "allergies", ["name"], unique=True)

    # 2. Create dietary_preferences table
    op.create_table(
        "dietary_preferences",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("description", sa.String(length=255), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("idx_dietary_preferences_name"),
        "dietary_preferences",
        ["name"],
        unique=True,
    )

    # 3. Create activity_levels table
    op.create_table(
        "activity_levels",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("name", sa.String(length=50), nullable=False),
        sa.Column("description", sa.String(length=255), nullable=True),
        sa.Column("multiplier", sa.Numeric(precision=4, scale=3), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("idx_activity_levels_name"), "activity_levels", ["name"], unique=True
    )

    # 4. Create users table
    op.create_table(
        "users",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("hashed_password", sa.String(length=255), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("is_superuser", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("idx_users_email"), "users", ["email"], unique=True)

    # 5. Create user_profiles table
    op.create_table(
        "user_profiles",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column("first_name", sa.String(length=100), nullable=True),
        sa.Column("last_name", sa.String(length=100), nullable=True),
        sa.Column("phone_number", sa.String(length=30), nullable=True),
        sa.Column("gender", sa.String(length=20), nullable=True),
        sa.Column("date_of_birth", sa.Date(), nullable=True),
        sa.Column("height", sa.Numeric(precision=5, scale=2), nullable=True),
        sa.Column("weight", sa.Numeric(precision=5, scale=2), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("user_id"),
    )
    op.create_index(
        op.f("idx_user_profiles_phone_number"),
        "user_profiles",
        ["phone_number"],
        unique=True,
    )

    # 6. Create user_goals table
    op.create_table(
        "user_goals",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column("goal_type", sa.String(length=50), nullable=False),
        sa.Column("target_weight", sa.Numeric(precision=5, scale=2), nullable=True),
        sa.Column("target_calories", sa.Integer(), nullable=True),
        sa.Column("target_protein", sa.Numeric(precision=5, scale=2), nullable=True),
        sa.Column("target_carbs", sa.Numeric(precision=5, scale=2), nullable=True),
        sa.Column("target_fat", sa.Numeric(precision=5, scale=2), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )

    # 7. Create user_preferences table
    op.create_table(
        "user_preferences",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column("language", sa.String(length=10), nullable=False),
        sa.Column("units_system", sa.String(length=20), nullable=False),
        sa.Column("daily_reminder_enabled", sa.Boolean(), nullable=False),
        sa.Column("daily_reminder_time", sa.Time(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("user_id"),
    )

    # 8. Create weight_history table
    op.create_table(
        "weight_history",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column("weight", sa.Numeric(precision=5, scale=2), nullable=False),
        sa.Column("logged_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )

    # 9. Create user_sessions table
    op.create_table(
        "user_sessions",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column("user_agent", sa.String(length=255), nullable=True),
        sa.Column("ip_address", sa.String(length=50), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )

    # 10. Create refresh_tokens table
    op.create_table(
        "refresh_tokens",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column("token", sa.String(length=512), nullable=False),
        sa.Column("is_revoked", sa.Boolean(), nullable=False),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("idx_refresh_tokens_token"), "refresh_tokens", ["token"], unique=True
    )

    # 11. Create audit_logs table
    op.create_table(
        "audit_logs",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("user_id", sa.UUID(), nullable=True),
        sa.Column("action", sa.String(length=100), nullable=False),
        sa.Column("ip_address", sa.String(length=50), nullable=True),
        sa.Column("details", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
    )

    # 12. Create user_allergies table
    op.create_table(
        "user_allergies",
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column("allergy_id", sa.UUID(), nullable=False),
        sa.ForeignKeyConstraint(["allergy_id"], ["allergies.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("user_id", "allergy_id"),
    )

    # 13. Create user_dietary_preferences table
    op.create_table(
        "user_dietary_preferences",
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column("dietary_preference_id", sa.UUID(), nullable=False),
        sa.ForeignKeyConstraint(
            ["dietary_preference_id"], ["dietary_preferences.id"], ondelete="CASCADE"
        ),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("user_id", "dietary_preference_id"),
    )


def downgrade() -> None:
    op.drop_table("user_dietary_preferences")
    op.drop_table("user_allergies")
    op.drop_table("audit_logs")
    op.drop_index(op.f("idx_refresh_tokens_token"), table_name="refresh_tokens")
    op.drop_table("refresh_tokens")
    op.drop_table("user_sessions")
    op.drop_table("weight_history")
    op.drop_table("user_preferences")
    op.drop_table("user_goals")
    op.drop_index(op.f("idx_user_profiles_phone_number"), table_name="user_profiles")
    op.drop_table("user_profiles")
    op.drop_index(op.f("idx_users_email"), table_name="users")
    op.drop_table("users")
    op.drop_index(op.f("idx_activity_levels_name"), table_name="activity_levels")
    op.drop_table("activity_levels")
    op.drop_index(
        op.f("idx_dietary_preferences_name"), table_name="dietary_preferences"
    )
    op.drop_table("dietary_preferences")
    op.drop_index(op.f("idx_allergies_name"), table_name="allergies")
    op.drop_table("allergies")
