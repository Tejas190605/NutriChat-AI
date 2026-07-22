import pytest
from httpx import AsyncClient
from uuid import uuid4
from sqlalchemy.ext.asyncio import AsyncSession
from src.services.auth_service import AuthService
from src.models.food import Food
from src.models.nutrition_fact import NutritionFact
from src.models.nutrition_profile import NutritionProfile


@pytest.mark.asyncio
async def test_nutrition_api_endpoints(client: AsyncClient, db_session: AsyncSession) -> None:
    """Verifies that all food lookup and favorites API handlers process request inputs correctly."""
    if db_session is None:
        pytest.skip("Database is offline")

    email = f"nutri_user_{uuid4()}@nutrichat.ai"
    password = "secure_password_123"

    auth_service = AuthService(db_session)
    user = await auth_service.register_user(email, password)
    access_token = auth_service.create_access_token(user.id)
    headers = {"Authorization": f"Bearer {access_token}"}

    # Setup database seed values for bananas food item query
    fact = NutritionFact(
        calories=90,
        protein=1.0,
        carbs=20.0,
        fat=0.3,
        fiber=1.0,
        sugar=12.0,
        sodium=1.0,
        saturated_fat=0.1,
    )
    db_session.add(fact)
    await db_session.flush()

    food = Food(name="Sweet Banana", description="Banana lookup item")
    db_session.add(food)
    await db_session.flush()

    profile = NutritionProfile(food_id=food.id, nutrition_fact_id=fact.id)
    db_session.add(profile)
    await db_session.flush()

    # 1. Lookup banana
    lookup_response = await client.get(
        "/api/v1/nutrition/lookup",
        headers=headers,
        params={"query": "Sweet"}
    )
    assert lookup_response.status_code == 200
    assert len(lookup_response.json()) == 1
    assert lookup_response.json()[0]["name"] == "Sweet Banana"

    # 2. Add Favorite
    fav_response = await client.post(
        f"/api/v1/nutrition/favorites/{food.id}",
        headers=headers,
    )
    assert fav_response.status_code == 201

    # 3. List Favorites
    fav_list = await client.get(
        "/api/v1/nutrition/favorites",
        headers=headers,
    )
    assert fav_list.status_code == 200
    assert len(fav_list.json()) == 1

    # 4. Remove Favorite
    remove_response = await client.delete(
        f"/api/v1/nutrition/favorites/{food.id}",
        headers=headers,
    )
    assert remove_response.status_code == 204
