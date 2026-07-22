from sqlalchemy import Column, ForeignKey, Table

from src.db.base import Base

user_allergies = Table(
    "user_allergies",
    Base.metadata,
    Column("user_id", ForeignKey("users.id", ondelete="CASCADE"), primary_key=True),
    Column(
        "allergy_id", ForeignKey("allergies.id", ondelete="CASCADE"), primary_key=True
    ),
)

user_dietary_preferences = Table(
    "user_dietary_preferences",
    Base.metadata,
    Column("user_id", ForeignKey("users.id", ondelete="CASCADE"), primary_key=True),
    Column(
        "dietary_preference_id",
        ForeignKey("dietary_preferences.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)
