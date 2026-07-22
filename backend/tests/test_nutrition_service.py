import pytest
from uuid import uuid4
from sqlalchemy.ext.asyncio import AsyncSession
from src.services.nutrition_service import NutritionService
from src.repositories.nutrition import FoodRepository
from src.models.food import Food
from src.models.nutrition_fact import NutritionFact
from src.models.nutrition_profile import NutritionProfile
from src.models.barcode import BarcodeProduct


@pytest.mark.asyncio
async def test_nutrition_lookups_and_favorites(db_session: AsyncSession) -> None:
    """Verifies that food, barcode queries, and favorites settings operate correctly."""
    if db_session is None:
        pytest.skip("Database is offline")

    user_id = uuid4()
    service = NutritionService(db_session)
    food_repo = FoodRepository(db_session)

    # 1. Create a food item inside catalog for lookup
    fact = NutritionFact(
        calories=100,
        protein=2.0,
        carbs=22.0,
        fat=0.5,
        fiber=1.5,
        sugar=10.0,
        sodium=5.0,
        saturated_fat=0.1,
    )
    db_session.add(fact)
    await db_session.flush()

    food = Food(
        name="Banana",
        description="Fresh banana fruits",
    )
    db_session.add(food)
    await db_session.flush()

    profile = NutritionProfile(
        food_id=food.id,
        nutrition_fact_id=fact.id,
    )
    db_session.add(profile)
    await db_session.flush()

    # 2. Query lookup text
    matches = await service.lookup_food("ban")
    assert len(matches) >= 1
    assert matches[0].name == "Banana"

    # 3. Barcode query lookup
    barcode_product = BarcodeProduct(
        barcode="88888888",
        product_name="Oreo Cookies",
        nutrition_fact_id=fact.id,
    )
    db_session.add(barcode_product)
    await db_session.flush()

    product = await service.lookup_barcode("88888888")
    assert product is not None
    assert product.product_name == "Oreo Cookies"

    # 4. Add Favorite
    fav = await service.add_favorite_food(user_id, food.id)
    assert fav.food_id == food.id

    favorites = await service.get_favorite_foods(user_id)
    assert len(favorites) == 1
    assert favorites[0].food.name == "Banana"

    # 5. Remove Favorite
    success = await service.remove_favorite_food(user_id, food.id)
    assert success is True
    assert len(await service.get_favorite_foods(user_id)) == 0
