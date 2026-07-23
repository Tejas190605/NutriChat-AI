from uuid import uuid4

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from src.services.auth_service import AuthService


@pytest.mark.asyncio
async def test_ai_persistence_api_endpoints(
    client: AsyncClient, db_session: AsyncSession
) -> None:
    """Verifies that all CRUD endpoints in the AI persistence API layer function correctly."""
    if db_session is None:
        pytest.skip("Database is offline")

    email = f"ai_user_{uuid4()}@nutrichat.ai"
    password = "secure_password_123"

    auth_service = AuthService(db_session)
    user = await auth_service.register_user(email, password)
    access_token = auth_service.create_access_token(user.id)
    headers = {"Authorization": f"Bearer {access_token}"}

    # 1. Start Conversation
    response = await client.post(
        "/api/v1/ai/conversations",
        headers=headers,
        json={"title": "Workout Planning"},
    )
    assert response.status_code == 201
    conv_data = response.json()
    assert conv_data["title"] == "Workout Planning"
    conv_id = conv_data["id"]

    # 2. List Conversations
    list_response = await client.get("/api/v1/ai/conversations", headers=headers)
    assert list_response.status_code == 200
    assert len(list_response.json()) >= 1

    # 3. Add Message
    msg_response = await client.post(
        f"/api/v1/ai/conversations/{conv_id}/messages",
        headers=headers,
        json={"role": "user", "content": "Need custom plan"},
    )
    assert msg_response.status_code == 201
    assert msg_response.json()["role"] == "user"

    # 4. Get Conversation details and history list
    get_response = await client.get(
        f"/api/v1/ai/conversations/{conv_id}", headers=headers
    )
    assert get_response.status_code == 200
    assert len(get_response.json()["messages"]) == 1

    # 5. Update Conversation
    update_response = await client.put(
        f"/api/v1/ai/conversations/{conv_id}",
        headers=headers,
        json={"title": "Updated Workout Planning", "is_active": False},
    )
    assert update_response.status_code == 200
    assert update_response.json()["title"] == "Updated Workout Planning"
    assert update_response.json()["is_active"] is False

    # 6. Delete Conversation
    delete_response = await client.delete(
        f"/api/v1/ai/conversations/{conv_id}", headers=headers
    )
    assert delete_response.status_code == 204

    # 7. Create Prompt Template
    template_name = f"template_{uuid4()}"
    tpl_response = await client.post(
        "/api/v1/ai/prompts/templates",
        headers=headers,
        json={"name": template_name, "description": "Custom prompt category template"},
    )
    assert tpl_response.status_code == 201
    tpl_data = tpl_response.json()
    tpl_id = tpl_data["id"]

    # 8. Create Prompt Version
    version_response = await client.post(
        f"/api/v1/ai/prompts/templates/{tpl_id}/versions",
        headers=headers,
        json={
            "version": 1,
            "system_prompt": "You are a specialized coach.",
            "user_prompt_template": "Track {param}",
            "model_name": "gemini-1.5-flash",
            "temperature": 0.5,
            "is_active": True,
        },
    )
    assert version_response.status_code == 201
    assert version_response.json()["is_active"] is True

    # 9. Get Active Prompt Version
    active_response = await client.get(
        f"/api/v1/ai/prompts/templates/{template_name}/active", headers=headers
    )
    assert active_response.status_code == 200
    assert active_response.json()["version"] == 1

    # 10. Log Recommendation
    rec_response = await client.post(
        "/api/v1/ai/recommendations",
        headers=headers,
        json={"category": "exercise", "content": {"advice": "Try swimming"}},
    )
    assert rec_response.status_code == 201
    rec_id = rec_response.json()["id"]

    # 11. Log Recommendation Feedback
    feedback_response = await client.post(
        f"/api/v1/ai/recommendations/{rec_id}/feedback",
        headers=headers,
        json={"feedback_value": "liked", "comments": "Thanks!"},
    )
    assert feedback_response.status_code == 201
