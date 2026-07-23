from uuid import uuid4

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession


@pytest.mark.asyncio
async def test_auth_api_routes(client: AsyncClient, db_session: AsyncSession) -> None:
    """Verifies that registration, login, token rotation, and logout endpoints function correctly."""
    if db_session is None:
        pytest.skip("Database is offline")

    email = f"api_user_{uuid4()}@nutrichat.ai"
    password = "super_secure_password_123"

    # 1. Register User
    reg_response = await client.post(
        "/api/v1/auth/register", json={"email": email, "password": password}
    )
    assert reg_response.status_code == 201
    reg_data = reg_response.json()
    assert reg_data["email"] == email
    assert "id" in reg_data

    # 2. Login User
    login_response = await client.post(
        "/api/v1/auth/login", json={"email": email, "password": password}
    )
    assert login_response.status_code == 200
    tokens = login_response.json()
    assert "access_token" in tokens
    assert "refresh_token" in tokens
    assert tokens["token_type"] == "bearer"

    # 3. Refresh Tokens
    refresh_response = await client.post(
        "/api/v1/auth/refresh", json={"refresh_token": tokens["refresh_token"]}
    )
    assert refresh_response.status_code == 200
    new_tokens = refresh_response.json()
    assert "access_token" in new_tokens
    assert "refresh_token" in new_tokens

    # 4. Logout User (Revokes refresh token)
    logout_response = await client.post(
        "/api/v1/auth/logout", json={"refresh_token": new_tokens["refresh_token"]}
    )
    assert logout_response.status_code == 204
