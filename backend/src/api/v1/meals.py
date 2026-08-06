from datetime import date, datetime, timedelta
from typing import Any
from uuid import UUID

import structlog
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.v1.deps import get_current_user
from src.db.session import get_async_session
from src.models.user import User
from src.schemas.meal import (
    DailySummaryResponse,
    MealCreateRequest,
    MealResponse,
    MealUpdateRequest,
    WeeklySummaryResponse,
)
from src.services.meal_service import MealService

logger = structlog.get_logger()
router = APIRouter()


@router.post(
    "/",
    response_model=MealResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Log a new meal with food items",
)
async def log_meal(
    payload: MealCreateRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_session),
) -> Any:
    """Inserts a new meal record and constituent items into the database."""
    meal_service = MealService(db)
    meal = await meal_service.log_meal(
        user_id=current_user.id,
        name=payload.name,
        items_data=payload.items,
        image_url=payload.image_url,
        logged_at=payload.logged_at,
    )
    return meal


@router.get(
    "/",
    response_model=list[MealResponse],
    status_code=status.HTTP_200_OK,
    summary="Get user logged meals list",
)
async def get_user_meals(
    date_str: str | None = Query(default=None, alias="date", description="Target date in YYYY-MM-DD format"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_session),
) -> Any:
    """Retrieves user's logged meals for a specific date or recent period."""
    meal_service = MealService(db)
    if date_str:
        try:
            target_date = date.fromisoformat(date_str)
        except ValueError:
            target_date = date.today()
    else:
        target_date = date.today()

    start_dt = datetime.combine(target_date - timedelta(days=7), datetime.min.time(), tzinfo=UTC)
    end_dt = datetime.combine(target_date, datetime.max.time(), tzinfo=UTC)

    return await meal_service.get_meal_history(current_user.id, start_dt, end_dt)


@router.get(
    "/history",
    response_model=list[MealResponse],
    status_code=status.HTTP_200_OK,
    summary="Get user meal history logs",
)
async def get_meal_history(
    start_date: datetime = Query(..., description="Start range datetime"),
    end_date: datetime = Query(..., description="End range datetime"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_session),
) -> Any:
    """Retrieves user's logged meals within a timestamp range, skipping soft deleted items."""
    meal_service = MealService(db)
    history = await meal_service.get_meal_history(current_user.id, start_date, end_date)
    return history


@router.get(
    "/daily-summary",
    response_model=DailySummaryResponse,
    status_code=status.HTTP_200_OK,
    summary="Retrieve daily macro totals vs targets progress",
)
async def get_daily_summary(
    day: date | None = Query(
        default=None, description="Target date (defaults to today)"
    ),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_session),
) -> Any:
    """Aggregates logged calories and macros consumed for a target date."""
    meal_service = MealService(db)
    target_day = day if day is not None else date.today()
    summary = await meal_service.get_daily_summary(current_user.id, target_day)
    return summary


@router.get(
    "/weekly-summary",
    response_model=WeeklySummaryResponse,
    status_code=status.HTTP_200_OK,
    summary="Retrieve weekly macro averages trends",
)
async def get_weekly_summary(
    start_date: date | None = Query(
        default=None, description="Weekly start date (defaults to 6 days ago)"
    ),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_session),
) -> Any:
    """Computes daily averages and details for a 7-day period starting on start_date."""
    meal_service = MealService(db)
    target_start = (
        start_date if start_date is not None else (date.today() - timedelta(days=6))
    )
    summary = await meal_service.get_weekly_summary(current_user.id, target_start)
    return summary


@router.put(
    "/{meal_id}",
    response_model=MealResponse,
    status_code=status.HTTP_200_OK,
    summary="Edit portions or items of a logged meal",
)
async def edit_meal(
    meal_id: UUID,
    payload: MealUpdateRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_session),
) -> Any:
    """Modifies logged meal details, updating child portion inputs."""
    meal_service = MealService(db)
    try:
        meal = await meal_service.edit_meal(
            user_id=current_user.id,
            meal_id=meal_id,
            name=payload.name,
            items_data=payload.items,
            image_url=payload.image_url,
        )
        return meal
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        ) from e


@router.delete(
    "/{meal_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Soft delete a logged meal",
)
async def delete_meal(
    meal_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_session),
) -> None:
    """Soft deletes a meal log from user history tracking."""
    meal_service = MealService(db)
    success = await meal_service.delete_meal(current_user.id, meal_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Meal not found or unauthorized",
        )
