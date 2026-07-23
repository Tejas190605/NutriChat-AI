from datetime import date, timedelta
from typing import Any
from uuid import UUID

import structlog
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.analytics_summary import DailyNutritionSummary
from src.repositories.user import UserRepository

logger = structlog.get_logger()


class PredictionEngine:
    """Predicts weight progression rates and goal dates using daily caloric surplus/deficits statistics."""

    def __init__(self, db: AsyncSession) -> None:
        self.db = db
        self.user_repo = UserRepository(db)

    async def predict_weight_trend(
        self, user_id: UUID, days_forecast: int = 30
    ) -> list[dict[str, Any]]:
        """Extrapolates weight targets using historic logging compliance logs.

        Rule: 7700 kcal deficit/surplus translates approximately to 1kg weight variance.
        """
        user = await self.user_repo.get(user_id)
        if not user or not user.profile:
            return []

        profile = user.profile
        start_weight = float(profile.weight) if profile.weight else 70.0

        # Determine average calorie deficit/surplus over last 14 days
        today = date.today()
        start_date = today - timedelta(days=14)

        stmt = (
            select(DailyNutritionSummary)
            .filter(DailyNutritionSummary.user_id == user_id)
            .filter(DailyNutritionSummary.date >= start_date)
        )
        res = await self.db.execute(stmt)
        summaries = res.scalars().all()

        active_goal = None
        for g in user.goals:
            if g.is_active:
                active_goal = g
                break
        target_cal = (
            float(active_goal.target_calories)
            if (active_goal and active_goal.target_calories)
            else 2000.0
        )

        daily_diffs = []
        for s in summaries:
            consumed = float(s.total_calories)
            # Deficit is (target_cal - consumed)
            daily_diffs.append(target_cal - consumed)

        avg_daily_deficit = (
            sum(daily_diffs) / len(daily_diffs) if daily_diffs else 300.0
        )  # baseline fallback

        forecast = []
        current_weight = start_weight
        for i in range(1, days_forecast + 1):
            forecast_date = today + timedelta(days=i)
            # Accumulate weight changes (deficit of 7700 kcal = 1kg lost)
            weight_change = avg_daily_deficit / 7700.0
            current_weight = current_weight - weight_change
            forecast.append(
                {
                    "date": forecast_date.isoformat(),
                    "predicted_weight": round(current_weight, 2),
                    "confidence_low": round(current_weight - 0.5, 2),
                    "confidence_high": round(current_weight + 0.5, 2),
                }
            )

        return forecast

    async def predict_goal_date(self, user_id: UUID) -> date | None:
        """Forecasts estimated completion date of user weight goals."""
        user = await self.user_repo.get(user_id)
        if not user or not user.profile or not user.goals:
            return None

        profile = user.profile
        active_goal = None
        for g in user.goals:
            if g.is_active:
                active_goal = g
                break
        if not active_goal or not active_goal.target_weight:
            return None

        current_weight = (
            float(profile.weight) if profile.weight else 70.0
        )
        target_weight = float(active_goal.target_weight)

        weight_diff = target_weight - current_weight
        if abs(weight_diff) < 0.1:
            return date.today()

        # Determine average weight loss speed based on historic logging
        today = date.today()
        start_date = today - timedelta(days=14)

        stmt = (
            select(DailyNutritionSummary)
            .filter(DailyNutritionSummary.user_id == user_id)
            .filter(DailyNutritionSummary.date >= start_date)
        )
        res = await self.db.execute(stmt)
        summaries = res.scalars().all()

        target_cal = (
            float(active_goal.target_calories)
            if active_goal.target_calories
            else 2000.0
        )
        daily_diffs = []
        for s in summaries:
            daily_diffs.append(target_cal - float(s.total_calories))

        avg_daily_deficit = (
            sum(daily_diffs) / len(daily_diffs) if daily_diffs else 300.0
        )

        # kg lost per day = deficit / 7700
        # If target weight requires a loss but we are in a surplus (deficit < 0), return None (plateau/mismatch)
        # If target weight requires a gain but we are in a deficit (deficit > 0), return None
        if weight_diff < 0 and avg_daily_deficit <= 0:
            return None
        if weight_diff > 0 and avg_daily_deficit >= 0:
            return None

        # Deficit rate calculations
        days_required = abs(weight_diff) / (abs(avg_daily_deficit) / 7700.0)

        if days_required > 365 * 2:  # capping at 2 years
            return None

        return today + timedelta(days=int(days_required))
