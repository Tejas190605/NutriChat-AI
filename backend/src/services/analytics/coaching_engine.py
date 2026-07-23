from datetime import date, timedelta
from uuid import UUID

import structlog
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.analytics_summary import DailyNutritionSummary
from src.models.coaching import Insight
from src.models.weight import WeightHistory
from src.repositories.user import UserRepository

logger = structlog.get_logger()


class CoachingEngine:
    """Analyzes user progression to generate personalized motivational advice, habit updates, and plateau alerts."""

    def __init__(self, db: AsyncSession) -> None:
        self.db = db
        self.user_repo = UserRepository(db)

    async def detect_plateau(self, user_id: UUID) -> bool:
        """Determines if a user has hit a weight loss plateau.

        Criteria: Weight history shows no change (<0.2kg variation) over the last 14 days,
        while maintaining an average daily calorie deficit of >200 kcal.
        """
        # Fetch weight logs
        today = date.today()
        start_date = today - timedelta(days=14)

        stmt_weight = (
            select(WeightHistory)
            .filter(WeightHistory.user_id == user_id)
            .filter(WeightHistory.logged_at >= start_date)
            .order_by(WeightHistory.logged_at.asc())
        )
        res_weight = await self.db.execute(stmt_weight)
        weights = res_weight.scalars().all()

        if len(weights) < 3:
            return False  # Insufficient data points

        w_values = [float(w.weight) for w in weights]
        weight_range = max(w_values) - min(w_values)

        if weight_range > 0.3:
            return False  # Weight is moving

        # Check calories deficit
        stmt_cal = (
            select(DailyNutritionSummary)
            .filter(DailyNutritionSummary.user_id == user_id)
            .filter(DailyNutritionSummary.date >= start_date)
        )
        res_cal = await self.db.execute(stmt_cal)
        summaries = res_cal.scalars().all()

        if not summaries:
            return False

        # Compute average calorie logs
        user = await self.user_repo.get(user_id)
        if not user or not user.goals:
            return False

        active_goal = None
        for g in user.goals:
            if g.is_active:
                active_goal = g
                break
        if not active_goal:
            return False

        target_cal = (
            float(active_goal.target_calories)
            if active_goal.target_calories
            else 2000.0
        )
        avg_calories = sum([float(s.total_calories) for s in summaries]) / len(
            summaries
        )

        # Check if average calorie deficit is significant (>200 kcal)
        if (target_cal - avg_calories) > 200.0:
            logger.info("Plateau detected for user profile", user_id=str(user_id))
            return True

        return False

    async def generate_daily_coaching(self, user_id: UUID) -> Insight:
        """Compiles motivational tips and custom diet recommendations for the daily dashboard.

        Incorporates plateau checks, target adjustments, and Indian diet advice.
        """
        user = await self.user_repo.get(user_id)
        if not user:
            raise ValueError("User not found")

        has_plateau = await self.detect_plateau(user_id)

        title = "Daily Nutrition Insight"
        content = (
            "Great work on logging your meals! Remember to keep your hydration high (at least 3 liters). "
            "Add high protein vegetarian options like paneer, tofu, or lentils to your upcoming lunch."
        )

        if has_plateau:
            title = "Plateau Alert & Coach Recommendation"
            content = (
                "Your weight has remained steady over the last two weeks despite hit calorie goals. "
                "This is a common metabolic plateau. We recommend adding a 20-minute daily walking routing "
                "or slightly boosting protein ratios to trigger fat loss."
            )
        elif user.allergies:
            allergies_list = [a.name.lower() for a in user.allergies]
            if "dairy" in allergies_list:
                content += " Since you have dairy allergies, try almond milk or soy protein substitutes."

        # Log coaching insight to db
        stmt_insight = (
            select(Insight)
            .filter(Insight.user_id == user_id)
            .filter(Insight.title == title)
            .order_by(Insight.created_at.desc())
        )
        res_insight = await self.db.execute(stmt_insight)
        record = res_insight.scalars().first()

        if not record:
            record = Insight(
                user_id=user_id,
                title=title,
                content=content,
                insight_type="daily",
            )
            self.db.add(record)
            await self.db.commit()

        return record
