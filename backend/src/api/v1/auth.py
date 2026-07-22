from typing import Any

import structlog
from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.session import get_async_session
from src.schemas.auth import (
    TokenRefreshRequest,
    TokenResponse,
    UserLoginRequest,
    UserRegisterRequest,
)
from src.schemas.user import UserResponse
from src.services.auth_service import AuthService

logger = structlog.get_logger()
router = APIRouter()


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new system user",
)
async def register(
    payload: UserRegisterRequest,
    db: AsyncSession = Depends(get_async_session),
) -> Any:
    """Creates a new user record with hashed password credentials."""
    auth_service = AuthService(db)
    try:
        user = await auth_service.register_user(payload.email, payload.password)
        await auth_service.log_audit(
            user_id=user.id,
            action="register",
            ip_address=None,
            details=f"Email registered: {payload.email}",
        )
        return user
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        ) from e


@router.post(
    "/login",
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK,
    summary="Authenticate credentials and issue JWT tokens",
)
async def login(
    payload: UserLoginRequest,
    request: Request,
    db: AsyncSession = Depends(get_async_session),
) -> Any:
    """Verifies password credentials, maps login session metadata, and issues access/refresh tokens."""
    auth_service = AuthService(db)
    user = await auth_service.authenticate_user(payload.email, payload.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )

    # Issue token pairs
    access_token = auth_service.create_access_token(user.id)
    refresh_token = await auth_service.create_refresh_token(user.id)

    # Log session details
    ip_address = request.client.host if request.client else None
    user_agent = request.headers.get("user-agent")
    await auth_service.create_user_session(user.id, user_agent, ip_address)

    # Audit log
    await auth_service.log_audit(
        user_id=user.id,
        action="login",
        ip_address=ip_address,
        details=f"Successful login for {payload.email}",
    )

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


@router.post(
    "/refresh",
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK,
    summary="Rotate refresh tokens",
)
async def refresh(
    payload: TokenRefreshRequest,
    db: AsyncSession = Depends(get_async_session),
) -> Any:
    """Validates refresh token signatures, revokes them, and yields a new access/refresh set."""
    auth_service = AuthService(db)
    try:
        new_access, new_refresh = await auth_service.rotate_tokens(
            payload.refresh_token
        )
        return {
            "access_token": new_access,
            "refresh_token": new_refresh,
            "token_type": "bearer",
        }
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
        ) from e


@router.post(
    "/logout",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Revoke active refresh credentials",
)
async def logout(
    payload: TokenRefreshRequest,
    db: AsyncSession = Depends(get_async_session),
) -> None:
    """Revokes refresh tokens from authentication database table, disabling sessions."""
    auth_service = AuthService(db)
    await auth_service.revoke_token(payload.refresh_token)
