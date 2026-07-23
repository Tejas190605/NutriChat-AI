import math
from datetime import date
from uuid import UUID

import structlog
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.analytics_summary import DailyNutritionSummary
from src.models.progress import BodyMeasurement, ProgressSnapshot
from src.repositories.base import BaseRepository
from src.repositories.user import UserRepository
from src.services.meal_service import MealService

logger = structlog.get_logger()


class AnalyticsEngine:
    """Calculates nutritional summary records, BMI indices, US Navy Body Fat percentages, and macro adherence metrics."""

    def __init__(self, db: AsyncSession) -> None:
        self.db = db
        self.user_repo = UserRepository(db)
        self.meal_service = MealService(db)
        self.summary_repo = BaseRepository(DailyNutritionSummary, db)
        self.measurement_repo = BaseRepository(BodyMeasurement, db)
        self.snapshot_repo = BaseRepository(ProgressSnapshot, db)

    async def calculate_daily_nutrition_summary(
        self, user_id: UUID, target_date: date
    ) -> DailyNutritionSummary:
        """Aggregates all meal logs for a date and saves/updates the DailyNutritionSummary database record."""
        summary_data = await self.meal_service.get_daily_summary(user_id, target_date)

        # Check if daily summary already exists
        stmt = (
            select(DailyNutritionSummary)
            .filter(DailyNutritionSummary.user_id == user_id)
            .filter(DailyNutritionSummary.date == target_date)
        )
        res = await self.db.execute(stmt)
        record = res.scalars().first()

        payload = {
            "user_id": user_id,
            "date": target_date,
            "total_calories": summary_data["consumed_calories"],
            "total_protein": summary_data["consumed_protein"],
            "total_carbs": summary_data["consumed_carbs"],
            "total_fat": summary_data["consumed_fat"],
            "total_fiber": 0.0,  # placeholder defaults
            "total_water_ml": 0,
        }

        if record:
            updated = await self.summary_repo.update(record, payload)
            return updated
        else:
            created = await self.summary_repo.create(payload)
            return created

    async def estimate_navy_body_fat(
        self, user_id: UUID, target_date: date
    ) -> float | None:
        """Calculates body fat percentage based on US Navy Circumference formulas.

        Formula (using centimeters):
        Males: Body Fat = 495 / (1.0324 - 0.19077 * log10(waist - neck) + 0.15456 * log10(height)) - 450
        Females: Body Fat = 495 / (1.29579 - 0.35004 * log10(waist + hip - neck) + 0.22100 * log10(height)) - 450
        """
        # Fetch user details
        user = await self.user_repo.get(user_id)
        if not user or not user.profile:
            return None

        profile = user.profile
        height = float(profile.height) if profile.height else None
        gender = profile.gender.lower() if profile.gender else "male"

        if not height or height <= 0:
            return None

        # Fetch body measurement records matching date
        stmt = (
            select(BodyMeasurement)
            .filter(BodyMeasurement.user_id == user_id)
            .filter(BodyMeasurement.date == target_date)
            .order_by(BodyMeasurement.created_at.desc())
        )
        res = await self.db.execute(stmt)
        measure = res.scalars().first()

        if not measure:
            # Fallback to the latest available measurement
            stmt_latest = (
                select(BodyMeasurement)
                .filter(BodyMeasurement.user_id == user_id)
                .order_by(BodyMeasurement.date.desc())
            )
            res_latest = await self.db.execute(stmt_latest)
            measure = res_latest.scalars().first()

        if not measure or not measure.waist or not measure.neck:
            return None

        waist = float(measure.waist)
        neck = float(measure.neck)
        hip = float(measure.hip) if measure.hip else 0.0

        try:
            if gender == "female":
                if hip <= 0 or (waist + hip - neck) <= 0:
                    return None
                density = (
                    1.29579
                    - 0.35004 * math.log10(waist + hip - neck)
                    + 0.22100 * math.log10(height)
                )
            else:
                if (waist - neck) <= 0:
                    return None
                density = (
                    1.0324
                    - 0.19077 * math.log10(waist - neck)
                    + 0.15456 * math.log10(height)
                )

            body_fat = (495.0 / density) - 450.0
            return max(2.0, round(body_fat, 2))
        except ValueError:
            logger.error(
                "Math error calculating US Navy Body Fat estimation values",
                user_id=str(user_id),
            )
            return None

    async def get_nutritional_score(self, user_id: UUID, target_date: date) -> float:
        """Deduces a score (0-100) assessing compliance compared to active UserGoal targets splits."""
        user = await self.user_repo.get(user_id)
        if not user or not user.goals:
            return 50.0  # baseline score

        active_goal = None
        for g in user.goals:
            if g.is_active:
                active_goal = g
                break
        if not active_goal:
            active_goal = user.goals[0]

        summary = await self.meal_service.get_daily_summary(user_id, target_date)
        consumed_cal = summary["consumed_calories"]
        target_cal = active_goal.target_calories or 2000

        if target_cal <= 0:
            return 100.0

        # Calculate deviation score
        variance = abs(target_cal - consumed_cal) / target_cal
        score = max(0.0, 100.0 - (variance * 100.0))
        return float(round(score, 1))
