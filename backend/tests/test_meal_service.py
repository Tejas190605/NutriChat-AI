from datetime import UTC, date, datetime
from uuid import uuid4

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas.meal import MealItemCreate
from src.services.meal_service import MealService


@pytest.mark.asyncio
async def test_meal_logs_and_nutrient_aggregation(db_session: AsyncSession) -> None:
    """Verifies that meal logging, editing, and daily totals calculations function correctly."""
    if db_session is None:
        pytest.skip("Database is offline")

    user_id = uuid4()
    service = MealService(db_session)

    # 1. Log Meal
    items = [
        MealItemCreate(
            food_name="Apple",
            quantity=1.0,
            unit="piece",
            calories=95,
            protein=0.5,
            carbs=25.0,
            fat=0.3,
        ),
        MealItemCreate(
            food_name="Oatmeal",
            quantity=1.0,
            unit="bowl",
            calories=150,
            protein=6.0,
            carbs=27.0,
            fat=3.0,
        ),
    ]

    meal = await service.log_meal(
        user_id=user_id,
        name="Breakfast",
        items_data=items,
        image_url="http://cloudinary.com/test.jpg",
    )

    assert meal.name == "Breakfast"
    assert meal.image_url == "http://cloudinary.com/test.jpg"
    assert len(meal.items) == 2
    assert meal.items[0].food_name in ["Apple", "Oatmeal"]

    # 2. Get Daily Summary
    today = date.today()
    summary = await service.get_daily_summary(user_id, today)
    assert summary["consumed_calories"] == 245
    assert summary["consumed_protein"] == 6.5
    assert summary["consumed_carbs"] == 52.0
    assert summary["consumed_fat"] == 3.3

    # 3. Edit Meal
    updated_items = [
        MealItemCreate(
            food_name="Apple",
            quantity=2.0,
            unit="piece",
            calories=190,
            protein=1.0,
            carbs=50.0,
            fat=0.6,
        ),
    ]
    edited = await service.edit_meal(
        user_id=user_id,
        meal_id=meal.id,
        name="Updated Breakfast",
        items_data=updated_items,
    )
    assert edited.name == "Updated Breakfast"
    assert len(edited.items) == 1
    assert edited.items[0].quantity == 2.0

    # 4. Soft Delete Meal
    success = await service.delete_meal(user_id, meal.id)
    assert success is True

    # 5. Eager query skipped soft deleted meal
    history = await service.get_meal_history(
        user_id,
        datetime.combine(today, datetime.min.time(), tzinfo=UTC),
        datetime.combine(today, datetime.max.time(), tzinfo=UTC),
    )
    assert len(history) == 0
