from typing import Any
from uuid import UUID

import structlog
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.v1.deps import get_current_user
from src.db.session import get_async_session
from src.models.user import User
from src.schemas.nutrition import (
    BarcodeProductResponse,
    FavoriteFoodResponse,
    FoodResponse,
    RecentFoodResponse,
)
from src.services.nutrition_service import NutritionService

logger = structlog.get_logger()
router = APIRouter()


@router.get(
    "/lookup",
    response_model=list[FoodResponse],
    status_code=status.HTTP_200_OK,
    summary="Query foods catalog by name",
)
async def lookup_food(
    query: str = Query(..., description="Food search name keyword"),
    limit: int = Query(default=20, description="Max lookup items limit"),
    _current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_session),
) -> Any:
    """Returns a list of matching foods from catalog matching text input."""
    service = NutritionService(db)
    foods = await service.lookup_food(query, limit)
    return foods


@router.get(
    "/barcode/{barcode}",
    response_model=BarcodeProductResponse,
    status_code=status.HTTP_200_OK,
    summary="Lookup packaged product by barcode",
)
async def lookup_barcode(
    barcode: str,
    _current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_session),
) -> Any:
    """Finds product mapping a scanned barcode, throwing 404 if untracked."""
    service = NutritionService(db)
    product = await service.lookup_barcode(barcode)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product barcode not found in catalog",
        )
    return product


@router.get(
    "/favorites",
    response_model=list[FavoriteFoodResponse],
    status_code=status.HTTP_200_OK,
    summary="Retrieve user favorite foods list",
)
async def get_favorites(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_session),
) -> Any:
    """Returns user's saved favorite food listings."""
    service = NutritionService(db)
    favorites = await service.get_favorite_foods(current_user.id)
    return favorites


@router.post(
    "/favorites/{food_id}",
    response_model=FavoriteFoodResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Add a food to favorites list",
)
async def add_favorite(
    food_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_session),
) -> Any:
    """Registers a food item inside user's favorites catalog preferences."""
    service = NutritionService(db)
    favorite = await service.add_favorite_food(current_user.id, food_id)
    return favorite


@router.delete(
    "/favorites/{food_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Remove a food from favorites list",
)
async def remove_favorite(
    food_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_session),
) -> None:
    """Deletes a food listing from user favorite configurations."""
    service = NutritionService(db)
    success = await service.remove_favorite_food(current_user.id, food_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Favorite food not found",
        )


@router.get(
    "/recents",
    response_model=list[RecentFoodResponse],
    status_code=status.HTTP_200_OK,
    summary="Get recently consumed foods list",
)
async def get_recents(
    limit: int = Query(default=10, description="Max logs retrieval size limit"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_session),
) -> Any:
    """Returns user recently logged items chronologically."""
    service = NutritionService(db)
    recents = await service.get_recent_foods(current_user.id, limit)
    return recents
