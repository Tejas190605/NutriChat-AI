from datetime import date
from typing import Any

import structlog
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.v1.deps import get_current_user
from src.db.session import get_async_session
from src.models.user import User
from src.services.analytics.analytics_engine import AnalyticsEngine
from src.services.analytics.coaching_engine import CoachingEngine
from src.services.analytics.prediction_engine import PredictionEngine
from src.services.analytics.recommendation_intel import RecommendationIntelligence

logger = structlog.get_logger()
router = APIRouter()


@router.get(
    "/daily",
    status_code=status.HTTP_200_OK,
    summary="Fetch daily dashboard nutrition totals and macro adherence score telemetry",
)
async def get_daily_dashboard(
    target_date: date = Query(default=None),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_session),
) -> Any:
    """Aggregates meal totals and calculates adherence compliance indices."""
    if not target_date:
        target_date = date.today()

    analytics = AnalyticsEngine(db)
    summary_record = await analytics.calculate_daily_nutrition_summary(
        current_user.id, target_date
    )
    score = await analytics.get_nutritional_score(current_user.id, target_date)

    return {
        "date": target_date.isoformat(),
        "total_calories": summary_record.total_calories,
        "total_protein": float(summary_record.total_protein),
        "total_carbs": float(summary_record.total_carbs),
        "total_fat": float(summary_record.total_fat),
        "nutritional_score": score,
    }


@router.get(
    "/weekly",
    status_code=status.HTTP_200_OK,
    summary="Fetch weekly trends summary",
)
async def get_weekly_trends(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_session),
) -> Any:
    """Returns weekly average macros metrics and body fat estimations."""
    analytics = AnalyticsEngine(db)
    body_fat = await analytics.estimate_navy_body_fat(current_user.id, date.today())

    return {
        "user_id": current_user.id,
        "body_fat_estimate": body_fat,
        "weekly_calories_average": 1800,  # mock baseline
        "weekly_compliance_rate": 85.0,
    }


@router.get(
    "/predictions",
    status_code=status.HTTP_200_OK,
    summary="Fetch weight trends predictions and goal dates forecasts",
)
async def get_predictions(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_session),
) -> Any:
    """Computes linear goal weight trajectories."""
    predictor = PredictionEngine(db)
    trend = await predictor.predict_weight_trend(current_user.id)
    goal_date = await predictor.predict_goal_date(current_user.id)

    return {
        "user_id": current_user.id,
        "predicted_goal_date": goal_date.isoformat() if goal_date else None,
        "forecast_trend": trend,
    }


@router.get(
    "/insights",
    status_code=status.HTTP_200_OK,
    summary="Fetch daily coaching tips and plateau warnings",
)
async def get_insights(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_session),
) -> Any:
    """Retrieves or creates daily coaching insight records."""
    coacher = CoachingEngine(db)
    insight = await coacher.generate_daily_coaching(current_user.id)

    return {
        "title": insight.title,
        "content": insight.content,
        "insight_type": insight.insight_type,
        "created_at": insight.created_at.isoformat(),
    }


@router.get(
    "/recommendations",
    status_code=status.HTTP_200_OK,
    summary="Fetch custom healthy swaps and snack suggestions",
)
async def get_recommendations(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_session),
) -> Any:
    """Compiles macro balances substitutions suggestions."""
    recommender = RecommendationIntelligence(db)
    macro_sug = await recommender.get_remaining_macro_suggestions(current_user.id)
    swaps = await recommender.get_healthy_substitutions(current_user.id)

    return {
        "macro_suggestions": macro_sug,
        "healthy_swaps": swaps,
    }
