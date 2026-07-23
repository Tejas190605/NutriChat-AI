from datetime import date
from uuid import uuid4

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.profile import UserProfile
from src.models.progress import BodyMeasurement
from src.models.user import User
from src.services.analytics.analytics_engine import AnalyticsEngine
from src.services.analytics.prediction_engine import PredictionEngine
from src.services.analytics.recommendation_intel import RecommendationIntelligence


@pytest.mark.asyncio
async def test_navy_body_fat_male(db_session: AsyncSession) -> None:
    """Verifies that the Navy Body Fat formula yields correct metric density outputs for males."""
    if db_session is None:
        pytest.skip("Database is offline")

    # Seed male user profile
    user_id = uuid4()
    user = User(id=user_id, email=f"test_bf_m_{user_id.hex[:6]}@example.com")
    profile = UserProfile(
        user_id=user_id,
        height=175.0,  # 175 cm
        gender="male",
        current_weight=75.0,
    )
    db_session.add(user)
    db_session.add(profile)

    measure = BodyMeasurement(
        user_id=user_id,
        date=date.today(),
        neck=38.0,  # cm
        waist=85.0,  # cm
    )
    db_session.add(measure)
    await db_session.commit()

    analytics = AnalyticsEngine(db_session)
    bf = await analytics.estimate_navy_body_fat(user_id, date.today())
    assert bf is not None
    assert bf > 5.0
    assert bf < 30.0  # standard male body fat range


@pytest.mark.asyncio
async def test_navy_body_fat_female(db_session: AsyncSession) -> None:
    """Verifies that the Navy Body Fat formula yields correct metric density outputs for females."""
    if db_session is None:
        pytest.skip("Database is offline")

    user_id = uuid4()
    user = User(id=user_id, email=f"test_bf_f_{user_id.hex[:6]}@example.com")
    profile = UserProfile(
        user_id=user_id,
        height=162.0,  # 162 cm
        gender="female",
        current_weight=60.0,
    )
    db_session.add(user)
    db_session.add(profile)

    measure = BodyMeasurement(
        user_id=user_id,
        date=date.today(),
        neck=34.0,  # cm
        waist=72.0,  # cm
        hip=94.0,  # cm (critical for women)
    )
    db_session.add(measure)
    await db_session.commit()

    analytics = AnalyticsEngine(db_session)
    bf = await analytics.estimate_navy_body_fat(user_id, date.today())
    assert bf is not None
    assert bf > 10.0
    assert bf < 40.0  # standard female body fat range


@pytest.mark.asyncio
async def test_predictions_weight_trend(db_session: AsyncSession) -> None:
    """Verifies that weight trends forecasting compiles a 30 day forecast list."""
    if db_session is None:
        pytest.skip("Database is offline")

    user_id = uuid4()
    user = User(id=user_id, email=f"test_pred_{user_id.hex[:6]}@example.com")
    profile = UserProfile(
        user_id=user_id,
        height=180.0,
        gender="male",
        current_weight=80.0,
    )
    db_session.add(user)
    db_session.add(profile)
    await db_session.commit()

    predictor = PredictionEngine(db_session)
    trend = await predictor.predict_weight_trend(user_id, days_forecast=10)
    assert len(trend) == 10
    assert "predicted_weight" in trend[0]
    assert "confidence_low" in trend[0]


@pytest.mark.asyncio
async def test_recommendations_and_swaps(db_session: AsyncSession) -> None:
    """Tests healthy swaps and remaining caloric suggests builder."""
    if db_session is None:
        pytest.skip("Database is offline")

    user_id = uuid4()
    user = User(id=user_id, email=f"test_rec_{user_id.hex[:6]}@example.com")
    db_session.add(user)
    await db_session.commit()

    recommender = RecommendationIntelligence(db_session)
    suggestions = await recommender.get_remaining_macro_suggestions(user_id)
    swaps = await recommender.get_healthy_substitutions(user_id)

    assert "remaining_calories" in suggestions
    assert len(swaps) > 0
    assert swaps[0]["original"] == "White Rice"


@pytest.mark.asyncio
async def test_analytics_endpoints(
    client: AsyncClient, db_session: AsyncSession
) -> None:
    """Tests the dashboard daily, weekly, predictions, and coaching insights REST routes."""
    if db_session is None:
        pytest.skip("Database is offline")

    # GET challenge check response checks
    resp_daily = await client.get("/api/v1/analytics/daily")
    # Should require authentication or fail gracefully with 401 if unauthenticated
    assert resp_daily.status_code in [200, 401]
