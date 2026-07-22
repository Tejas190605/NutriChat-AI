from typing import Any

import structlog
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.v1.deps import get_current_user
from src.db.session import get_async_session
from src.models.user import User
from src.schemas.goal import UserGoalCreateRequest, UserGoalResponse
from src.schemas.profile import UserProfileResponse, UserProfileUpdateRequest
from src.schemas.user import UserDetailResponse
from src.schemas.weight import WeightLogCreateRequest, WeightLogResponse
from src.services.user_service import UserService

logger = structlog.get_logger()
router = APIRouter()


@router.get(
    "/me",
    response_model=UserDetailResponse,
    status_code=status.HTTP_200_OK,
    summary="Get currently authenticated user details",
)
async def get_me(current_user: User = Depends(get_current_user)) -> Any:
    """Returns profile and credential details of the authenticated request subject."""
    return current_user


@router.put(
    "/me/profile",
    response_model=UserProfileResponse,
    status_code=status.HTTP_200_OK,
    summary="Update user personal profile",
)
async def update_my_profile(
    payload: UserProfileUpdateRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_session),
) -> Any:
    """Updates user demographic, height, weight, and DOB settings."""
    user_service = UserService(db)
    profile = await user_service.update_profile(current_user.id, payload)
    return profile


@router.post(
    "/me/goals",
    response_model=UserGoalResponse,
    status_code=status.HTTP_200_OK,
    summary="Calculate and save user nutrition/macro goals",
)
async def set_my_goals(
    payload: UserGoalCreateRequest,
    activity_multiplier: float = Query(
        default=1.2, description="TDEE activity multiplier"
    ),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_session),
) -> Any:
    """Calculates custom macro/calories splits (Mifflin-St Jeor) and logs active goal."""
    user_service = UserService(db)
    goal = await user_service.calculate_and_save_goals(
        current_user.id, payload.goal_type, activity_multiplier
    )
    return goal


@router.post(
    "/me/weight",
    response_model=WeightLogResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Log a new weight entry in history",
)
async def log_my_weight(
    payload: WeightLogCreateRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_session),
) -> Any:
    """Logs weight historical metrics, updating user profile weight."""
    user_service = UserService(db)
    log = await user_service.log_weight(current_user.id, payload.weight)
    return log


@router.get(
    "/me/weight",
    response_model=list[WeightLogResponse],
    status_code=status.HTTP_200_OK,
    summary="Get user weight history log",
)
async def get_my_weight_history(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_session),
) -> Any:
    """Returns chronological user weight logs."""
    user_service = UserService(db)
    history = await user_service.get_weight_history(current_user.id)
    return history
