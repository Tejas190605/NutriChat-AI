from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from src.models.category import FoodCategory
from src.models.favorite_food import FavoriteFood
from src.models.food import Food
from src.models.nutrition_profile import NutritionProfile
from src.models.recent_food import RecentFood
from src.repositories.base import BaseRepository


class FoodRepository(BaseRepository[Food]):
    """Repository for Food-related queries."""

    def __init__(self, db: AsyncSession):
        super().__init__(Food, db)

    async def search_by_name(self, query: str, limit: int = 20) -> list[Food]:
        """Performs case-insensitive searches for foods by name with nutrition facts preloaded."""
        stmt = (
            select(self.model)
            .filter(self.model.name.ilike(f"%{query}%"))
            .options(
                joinedload(Food.nutrition_profile).joinedload(
                    NutritionProfile.nutrition_fact
                )
            )
            .limit(limit)
        )
        res = await self.db.execute(stmt)
        return list(res.scalars().all())

    async def get_with_relations(self, id: UUID) -> Food | None:
        """Retrieves a food item preloading its nutrition profile and facts details."""
        stmt = (
            select(self.model)
            .filter(self.model.id == id)
            .options(
                joinedload(Food.nutrition_profile).joinedload(
                    NutritionProfile.nutrition_fact
                )
            )
        )
        res = await self.db.execute(stmt)
        return res.scalars().first()


class FoodCategoryRepository(BaseRepository[FoodCategory]):
    """Repository for FoodCategory database operations."""

    def __init__(self, db: AsyncSession):
        super().__init__(FoodCategory, db)


class FavoriteFoodRepository(BaseRepository[FavoriteFood]):
    """Repository for FavoriteFood queries."""

    def __init__(self, db: AsyncSession):
        super().__init__(FavoriteFood, db)

    async def get_user_favorites(self, user_id: UUID) -> list[FavoriteFood]:
        """Retrieves a user's favorite foods with full relationships eager loaded."""
        stmt = (
            select(self.model)
            .filter(self.model.user_id == user_id)
            .options(
                joinedload(FavoriteFood.food)
                .joinedload(Food.nutrition_profile)
                .joinedload(NutritionProfile.nutrition_fact)
            )
        )
        res = await self.db.execute(stmt)
        return list(res.scalars().all())

    async def get_by_user_and_food(
        self, user_id: UUID, food_id: UUID
    ) -> FavoriteFood | None:
        """Finds a favorite food listing by user and target food ID."""
        stmt = select(self.model).filter(
            self.model.user_id == user_id, self.model.food_id == food_id
        )
        res = await self.db.execute(stmt)
        return res.scalars().first()


class RecentFoodRepository(BaseRepository[RecentFood]):
    """Repository for RecentFood operations."""

    def __init__(self, db: AsyncSession):
        super().__init__(RecentFood, db)

    async def get_user_recents(
        self, user_id: UUID, limit: int = 10
    ) -> list[RecentFood]:
        """Retrieves recently logged foods chronologically."""
        stmt = (
            select(self.model)
            .filter(self.model.user_id == user_id)
            .options(
                joinedload(RecentFood.food)
                .joinedload(Food.nutrition_profile)
                .joinedload(NutritionProfile.nutrition_fact)
            )
            .order_by(self.model.last_used_at.desc())
            .limit(limit)
        )
        res = await self.db.execute(stmt)
        return list(res.scalars().all())

    async def get_by_user_and_food(
        self, user_id: UUID, food_id: UUID
    ) -> RecentFood | None:
        """Finds a recent food entry by user and food ID."""
        stmt = select(self.model).filter(
            self.model.user_id == user_id, self.model.food_id == food_id
        )
        res = await self.db.execute(stmt)
        return res.scalars().first()
