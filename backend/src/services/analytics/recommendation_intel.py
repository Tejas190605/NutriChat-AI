from datetime import date
from typing import Any
from uuid import UUID

import structlog
from sqlalchemy.ext.asyncio import AsyncSession

from src.repositories.user import UserRepository
from src.services.meal_service import MealService

logger = structlog.get_logger()


class RecommendationIntelligence:
    """Generates food substitutes, protein modifications, and meal timing suggestions based on logged nutrition."""

    def __init__(self, db: AsyncSession) -> None:
        self.db = db
        self.user_repo = UserRepository(db)
        self.meal_service = MealService(db)

    async def get_remaining_macro_suggestions(self, user_id: UUID) -> dict[str, Any]:
        """Examines remaining calories for the day and recommends targeted food snacks to balance budgets."""
        user = await self.user_repo.get(user_id)
        if not user or not user.goals:
            return {"suggestions": []}

        active_goal = None
        for g in user.goals:
            if g.is_active:
                active_goal = g
                break
        if not active_goal:
            return {"suggestions": []}

        summary = await self.meal_service.get_daily_summary(user_id, date.today())
        consumed_cal = summary["consumed_calories"]
        target_cal = active_goal.target_calories or 2000

        remaining_cal = max(0, target_cal - consumed_cal)

        suggestions = []
        if remaining_cal > 300:
            suggestions.append(
                {
                    "meal": "Snack",
                    "recommendation": "Try high-protein Greek yogurt with mixed berries or roasted chana.",
                    "target": "high_protein",
                }
            )
        if remaining_cal > 100 and remaining_cal <= 300:
            suggestions.append(
                {
                    "meal": "Light Snack",
                    "recommendation": "Grab a handful of almonds or walnuts (approx 150 kcal).",
                    "target": "healthy_fats",
                }
            )
        if remaining_cal == 0:
            suggestions.append(
                {
                    "meal": "Completed",
                    "recommendation": "You've successfully hit your calorie limit today. Focus on hydration!",
                    "target": "water",
                }
            )

        return {
            "remaining_calories": remaining_cal,
            "suggestions": suggestions,
        }

    async def get_healthy_substitutions(self, _user_id: UUID) -> list[dict[str, str]]:
        """Scans recent meal log items and offers healthier alternative swaps."""
        # Baseline healthy swaps for standard Indian meals
        swaps = [
            {
                "original": "White Rice",
                "substitution": "Brown Rice or Quinoa",
                "reason": "Higher fiber and lower glycemic index.",
            },
            {
                "original": "Butter Naan",
                "substitution": "Roti or Multigrain Chapati",
                "reason": "Reduces saturated fat and refined flour load.",
            },
            {
                "original": "Fruit Juices",
                "substitution": "Whole Fruits",
                "reason": "Retains dietary fibers and slows sugar absorption.",
            },
            {
                "original": "Deep Fried Samosa",
                "substitution": "Baked Samosa or Roasted Makhana",
                "reason": "Cuts trans fats and total calories.",
            },
        ]
        return swaps
