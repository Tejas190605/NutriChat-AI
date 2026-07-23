from datetime import date
from typing import Any
from uuid import UUID

import structlog
from sqlalchemy.ext.asyncio import AsyncSession

from src.repositories.user import UserRepository
from src.services.meal_service import MealService

logger = structlog.get_logger()


class RecommendationEngine:
    """Calculates remaining macronutrients budgets and generates target swaps and coaching suggestions."""

    def __init__(self, db: AsyncSession) -> None:
        self.db = db
        self.user_repo = UserRepository(db)
        self.meal_service = MealService(db)

    async def generate_macro_recommendations(self, user_id: UUID) -> dict[str, Any]:
        """Calculates deficits, remaining calories/macros, and returns healthy food swaps.

        Args:
            user_id: ID of the user.

        Returns:
            A dictionary matching goal progress and alternatives swaps.
        """
        user = await self.user_repo.get(user_id)
        if not user or user.deleted_at:
            raise ValueError(f"User not found: {user_id}")

        # Fetch active goal
        active_goal = None
        if user.goals:
            for g in user.goals:
                if g.is_active:
                    active_goal = g
                    break
            if not active_goal:
                active_goal = user.goals[0]

        if not active_goal:
            raise ValueError(
                "User goals and target splits not found. Complete onboarding first."
            )

        # Fetch today's consumed macros summary totals
        today = date.today()
        summary = await self.meal_service.get_daily_summary(user_id, today)

        # Target definitions
        target_cal = active_goal.target_calories or 2000
        target_prot = active_goal.target_protein or 120.0
        target_carbs = active_goal.target_carbs or 200.0
        target_fat = active_goal.target_fat or 65.0

        # Consumed values
        consumed_cal = summary["consumed_calories"]
        consumed_prot = summary["consumed_protein"]
        consumed_carbs = summary["consumed_carbs"]
        consumed_fat = summary["consumed_fat"]

        # Remaining calculations
        remaining_cal = max(0, target_cal - consumed_cal)
        remaining_prot = max(0.0, float(target_prot - consumed_prot))
        remaining_carbs = max(0.0, float(target_carbs - consumed_carbs))
        remaining_fat = max(0.0, float(target_fat - consumed_fat))

        # Personal coaching swaps suggestions based on target deficits
        alternatives = []
        if remaining_cal < 300:
            alternatives.append(
                {
                    "original": "Standard sweets or heavy desserts",
                    "alternative": "Greek yogurt with berries or a serving of roasted Makhana (fox nuts)",
                    "benefit": "Avoids excess carbohydrates while providing additional protein.",
                }
            )

        # General healthy Indian swaps
        alternatives.append(
            {
                "original": "White rice or standard rotis",
                "alternative": "Brown rice, Quinoa, or Oats Roti",
                "benefit": "Lower glycemic index and higher dietary fibers.",
            }
        )
        alternatives.append(
            {
                "original": "Butter Paneer Masala",
                "alternative": "Grilled Paneer Tikka or Tofu stir-fry",
                "benefit": "Reduces saturated fat intake while keeping protein high.",
            }
        )

        coaching_advice = "You are doing great! "
        if consumed_cal > target_cal:
            coaching_advice += "You have exceeded your calorie limit for today. Focus on light activity (e.g. 20 min walk) and low-calorie fiber-rich items."
        elif remaining_cal > 500:
            coaching_advice += f"You have {remaining_cal} kcal remaining. Consider adding a high-protein snack to reach your macro targets."
        else:
            coaching_advice += "You are right on track to achieve your weight target! Maintain this macro split consistency."

        result = {
            "user_id": str(user_id),
            "target_calories": target_cal,
            "consumed_calories": consumed_cal,
            "remaining_calories": remaining_cal,
            "macro_targets": {
                "protein": target_prot,
                "carbs": target_carbs,
                "fat": target_fat,
            },
            "macro_consumed": {
                "protein": consumed_prot,
                "carbs": consumed_carbs,
                "fat": consumed_fat,
            },
            "macro_remaining": {
                "protein": round(remaining_prot, 1),
                "carbs": round(remaining_carbs, 1),
                "fat": round(remaining_fat, 1),
            },
            "swaps_alternatives": alternatives,
            "coaching_advice": coaching_advice,
        }

        logger.info(
            "Macro recommendations generated",
            user_id=str(user_id),
            remaining_cal=remaining_cal,
        )
        return result
