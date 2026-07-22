from datetime import datetime
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.models.meal import Meal
from src.repositories.base import BaseRepository


class MealRepository(BaseRepository[Meal]):
    """Repository for Meal entities management."""

    def __init__(self, db: AsyncSession):
        super().__init__(Meal, db)

    async def get_meal_with_items(self, meal_id: UUID) -> Meal | None:
        """Retrieves a single meal eager loading its child food items."""
        stmt = (
            select(self.model)
            .filter(self.model.id == meal_id)
            .filter(self.model.deleted_at.is_(None))
            .options(selectinload(Meal.items))
        )
        res = await self.db.execute(stmt)
        return res.scalars().first()

    async def get_user_meals_in_range(
        self, user_id: UUID, start_dt: datetime, end_dt: datetime
    ) -> list[Meal]:
        """Retrieves active meals logged by a user within a timestamp range."""
        stmt = (
            select(self.model)
            .filter(self.model.user_id == user_id)
            .filter(self.model.logged_at >= start_dt)
            .filter(self.model.logged_at <= end_dt)
            .filter(self.model.deleted_at.is_(None))
            .options(selectinload(Meal.items))
            .order_by(self.model.logged_at.desc())
        )
        res = await self.db.execute(stmt)
        return list(res.scalars().all())
