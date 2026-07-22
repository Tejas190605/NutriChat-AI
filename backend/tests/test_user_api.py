import pytest
from httpx import AsyncClient
from uuid import uuid4
from sqlalchemy.ext.asyncio import AsyncSession
from src.services.auth_service import AuthService


@pytest.mark.asyncio
async def test_user_profile_and_goals_api(client: AsyncClient, db_session: AsyncSession) -> None:
    """Verifies that user profile, goal logging, and weight history endpoint operations behave correctly."""
    if db_session is None:
        pytest.skip("Database is offline")
        
    email = f"user_{uuid4()}@nutrichat.ai"
    password = "secure_password_123"

    auth_service = AuthService(db_session)
    user = await auth_service.register_user(email, password)
    access_token = auth_service.create_access_token(user.id)
    headers = {"Authorization": f"Bearer {access_token}"}

    # 1. Fetch Current User details (/me)
    me_response = await client.get("/api/v1/users/me", headers=headers)
    assert me_response.status_code == 200
    me_data = me_response.json()
    assert me_data["email"] == email

    # 2. Update Profile (/me/profile)
    profile_response = await client.put(
        "/api/v1/users/me/profile",
        headers=headers,
        json={
            "first_name": "Tejas",
            "last_name": "Sabnis",
            "gender": "male",
            "height": 180.0,
            "weight": 85.0,
        }
    )
    assert profile_response.status_code == 200
    profile_data = profile_response.json()
    assert profile_data["first_name"] == "Tejas"
    assert float(profile_data["height"]) == 180.0
    assert float(profile_data["weight"]) == 85.0

    # 3. Calculate and Save Goals (/me/goals)
    goal_response = await client.post(
        "/api/v1/users/me/goals",
        headers=headers,
        json={"goal_type": "weight_loss"}
    )
    assert goal_response.status_code == 200
    goal_data = goal_response.json()
    assert goal_data["goal_type"] == "weight_loss"
    assert goal_data["is_active"] is True
    assert goal_data["target_calories"] is not None

    # 4. Log Weight Entry (/me/weight)
    weight_response = await client.post(
        "/api/v1/users/me/weight",
        headers=headers,
        json={"weight": 84.5}
    )
    assert weight_response.status_code == 201
    weight_data = weight_response.json()
    assert float(weight_data["weight"]) == 84.5

    # 5. Fetch Weight History (/me/weight)
    history_response = await client.get("/api/v1/users/me/weight", headers=headers)
    assert history_response.status_code == 200
    history_data = history_response.json()
    assert len(history_data) == 2
    assert float(history_data[0]["weight"]) == 84.5
    assert float(history_data[1]["weight"]) == 85.0
