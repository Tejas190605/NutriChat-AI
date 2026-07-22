from uuid import UUID

import structlog
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.barcode import BarcodeProduct
from src.models.favorite_food import FavoriteFood
from src.models.food import Food
from src.models.recent_food import RecentFood
from src.repositories.barcode import BarcodeRepository
from src.repositories.nutrition import (
    FavoriteFoodRepository,
    FoodRepository,
    RecentFoodRepository,
)

logger = structlog.get_logger()


class NutritionService:
    """Service orchestrating food lookups, favorites preferences, and barcode lookups."""

    def __init__(self, db: AsyncSession):
        self.db = db
        self.food_repo = FoodRepository(db)
        self.barcode_repo = BarcodeRepository(db)
        self.favorite_repo = FavoriteFoodRepository(db)
        self.recent_repo = RecentFoodRepository(db)

    async def lookup_food(self, query: str, limit: int = 20) -> list[Food]:
        """Queries foods by name containing search string, preloading nutrition facts."""
        return await self.food_repo.search_by_name(query, limit)

    async def lookup_barcode(self, barcode: str) -> BarcodeProduct | None:
        """Finds barcode catalog entries matching scanned numbers."""
        return await self.barcode_repo.get_by_barcode(barcode)

    async def get_favorite_foods(self, user_id: UUID) -> list[FavoriteFood]:
        """Retrieves a user's logged favorite food listings."""
        return await self.favorite_repo.get_user_favorites(user_id)

    async def add_favorite_food(self, user_id: UUID, food_id: UUID) -> FavoriteFood:
        """Adds a food definition to the user's favorites list."""
        existing = await self.favorite_repo.get_by_user_and_food(user_id, food_id)
        if existing:
            return existing

        favorite = await self.favorite_repo.create(
            {
                "user_id": user_id,
                "food_id": food_id,
            }
        )
        return favorite

    async def remove_favorite_food(self, user_id: UUID, food_id: UUID) -> bool:
        """Removes a food entry from the user's favorites list."""
        favorite = await self.favorite_repo.get_by_user_and_food(user_id, food_id)
        if not favorite:
            return False

        await self.favorite_repo.remove(favorite.id)
        return True

    async def get_recent_foods(
        self, user_id: UUID, limit: int = 10
    ) -> list[RecentFood]:
        """Retrieves user recently logged foods list."""
        return await self.recent_repo.get_user_recents(user_id, limit)
