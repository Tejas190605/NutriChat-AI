import pytest
from httpx import AsyncClient
from uuid import uuid4
from sqlalchemy.ext.asyncio import AsyncSession
from src.services.auth_service import AuthService


@pytest.mark.asyncio
async def test_meals_api_endpoints(client: AsyncClient, db_session: AsyncSession) -> None:
    """Verifies all meal endpoint routes handle requests correctly."""
    if db_session is None:
        pytest.skip("Database is offline")

    email = f"meal_user_{uuid4()}@nutrichat.ai"
    password = "secure_password_123"

    auth_service = AuthService(db_session)
    user = await auth_service.register_user(email, password)
    access_token = auth_service.create_access_token(user.id)
    headers = {"Authorization": f"Bearer {access_token}"}

    # 1. Log Meal
    response = await client.post(
        "/api/v1/meals/",
        headers=headers,
        json={
            "name": "Lunch",
            "items": [
                {
                    "food_name": "Roti",
                    "quantity": 2.0,
                    "unit": "piece",
                    "calories": 180,
                    "protein": 6.0,
                    "carbs": 34.0,
                    "fat": 1.0,
                }
            ],
            "image_url": "http://image.url",
        }
    )
    assert response.status_code == 201
    meal_data = response.json()
    assert meal_data["name"] == "Lunch"
    meal_id = meal_data["id"]

    # 2. Fetch History
    hist_response = await client.get(
        "/api/v1/meals/history",
        headers=headers,
        params={
            "start_date": "2026-07-22T00:00:00Z",
            "end_date": "2026-07-24T00:00:00Z",
        }
    )
    assert hist_response.status_code == 200
    assert len(hist_response.json()) == 1

    # 3. Fetch Daily Summary
    daily_response = await client.get(
        "/api/v1/meals/daily-summary",
        headers=headers,
    )
    assert daily_response.status_code == 200
    assert daily_response.json()["consumed_calories"] == 180

    # 4. Fetch Weekly Summary
    weekly_response = await client.get(
        "/api/v1/meals/weekly-summary",
        headers=headers,
    )
    assert weekly_response.status_code == 200
    assert "daily_average" in weekly_response.json()

    # 5. Update Meal
    update_response = await client.put(
        f"/api/v1/meals/{meal_id}",
        headers=headers,
        json={
            "name": "Updated Lunch",
            "items": [
                {
                    "food_name": "Roti",
                    "quantity": 3.0,
                    "unit": "piece",
                    "calories": 270,
                    "protein": 9.0,
                    "carbs": 51.0,
                    "fat": 1.5,
                }
            ],
        }
    )
    assert update_response.status_code == 200
    assert update_response.json()["name"] == "Updated Lunch"

    # 6. Delete Meal
    delete_response = await client.delete(
        f"/api/v1/meals/{meal_id}",
        headers=headers,
    )
    assert delete_response.status_code == 204
