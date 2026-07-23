from uuid import uuid4

import jwt
import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from src.config.settings import settings
from src.services.auth_service import AuthService


@pytest.mark.asyncio
async def test_password_hashing() -> None:
    """Verifies that password hashing generates correct verification validations."""
    auth = AuthService(None)  # Session not required for pure hashing logic
    password = "secure_test_password"

    hashed = auth.hash_password(password)
    assert hashed != password
    assert auth.verify_password(hashed, password) is True
    assert auth.verify_password(hashed, "wrong_password") is False


@pytest.mark.asyncio
async def test_register_and_authenticate(db_session: AsyncSession) -> None:
    """Verifies user registration and credentials authentication flow."""
    if db_session is None:
        pytest.skip("Database is offline")

    auth = AuthService(db_session)
    email = f"user_{uuid4()}@nutrichat.ai"
    password = "secure_test_password"

    # Register
    user = await auth.register_user(email, password)
    assert user.email == email
    assert user.is_active is True

    # Duplicate registration should fail
    with pytest.raises(ValueError, match="already registered"):
        await auth.register_user(email, password)

    # Authenticate
    authenticated_user = await auth.authenticate_user(email, password)
    assert authenticated_user is not None
    assert authenticated_user.id == user.id

    # Wrong credentials
    assert await auth.authenticate_user(email, "wrong_password") is None
    assert await auth.authenticate_user("untracked@nutrichat.ai", password) is None


@pytest.mark.asyncio
async def test_token_issuance_and_rotation(db_session: AsyncSession) -> None:
    """Verifies JWT access and refresh token pair generation and rotation."""
    if db_session is None:
        pytest.skip("Database is offline")

    auth = AuthService(db_session)
    user_id = uuid4()

    # Generate tokens
    access = auth.create_access_token(user_id)
    refresh = await auth.create_refresh_token(user_id)

    assert access is not None
    assert refresh is not None

    # Verify Access payload
    payload = jwt.decode(
        access, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM]
    )
    assert payload["sub"] == str(user_id)
    assert payload["type"] == "access"

    # Rotate
    new_access, new_refresh = await auth.rotate_tokens(refresh)
    assert new_access != access
    assert new_refresh != refresh

    # Rotated token should be revoked and unusable
    with pytest.raises(ValueError, match="expired, revoked, or untracked"):
        await auth.rotate_tokens(refresh)
