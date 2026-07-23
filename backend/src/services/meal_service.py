import uuid
from datetime import UTC, date, datetime, timedelta
from typing import Any
from uuid import UUID

import structlog
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.food import Food
from src.models.goal import UserGoal
from src.models.meal import Meal
from src.models.meal_item import MealItem
from src.repositories.meal import MealRepository
from src.repositories.nutrition import FoodRepository, RecentFoodRepository
from src.schemas.meal import DailyMacros, MealItemCreate

logger = structlog.get_logger()


class MealService:
    """Service driving meal log persistence, updates, soft deletes, and nutrient summaries."""

    def __init__(self, db: AsyncSession):
        self.db = db
        self.meal_repo = MealRepository(db)
        self.recent_repo = RecentFoodRepository(db)
        self.food_repo = FoodRepository(db)

    async def log_meal(
        self,
        user_id: UUID,
        name: str,
        items_data: list[MealItemCreate],
        image_url: str | None = None,
        logged_at: datetime | None = None,
    ) -> Meal:
        """Creates a Meal log and inserts constituent food items, tracking recents list."""
        if not logged_at:
            logged_at = datetime.now(UTC)

        meal = await self.meal_repo.create(
            {
                "user_id": user_id,
                "name": name,
                "image_url": image_url,
                "logged_at": logged_at,
            }
        )

        for item in items_data:
            # Attempt to find matching food entity in database to link
            food = await self._find_food_by_name(item.food_name)
            food_id = food.id if food else None

            await self.db.execute(
                select(MealItem)
            )  # Warmup query placeholder to satisfy base mapping dependencies compiler

            # Create individual meal item row
            db_item = MealItem(
                id=uuid.uuid4(),
                meal_id=meal.id,
                food_id=food_id,
                food_name=item.food_name,
                quantity=item.quantity,
                unit=item.unit,
                weight_grams=item.weight_grams,
                calories=item.calories,
                protein=item.protein,
                carbs=item.carbs,
                fat=item.fat,
            )
            self.db.add(db_item)

            # Record / update in user's recently consumed list
            if food_id:
                await self._track_recent_food(user_id, food_id)

        await self.db.flush()
        # Eager load items to return complete structure
        ret_meal = await self.meal_repo.get_meal_with_items(meal.id)
        assert ret_meal is not None
        return ret_meal

    async def edit_meal(
        self,
        user_id: UUID,
        meal_id: UUID,
        name: str | None = None,
        items_data: list[MealItemCreate] | None = None,
        image_url: str | None = None,
    ) -> Meal:
        """Updates active meal fields, replacing child items if list is provided."""
        meal = await self.meal_repo.get_meal_with_items(meal_id)
        if not meal or meal.user_id != user_id or meal.deleted_at:
            raise ValueError("Meal not found or unauthorized")

        update_dict = {}
        if name is not None:
            update_dict["name"] = name
        if image_url is not None:
            update_dict["image_url"] = image_url

        if update_dict:
            await self.meal_repo.update(meal, update_dict)

        if items_data is not None:
            # Delete old items
            for old_item in meal.items:
                await self.db.delete(old_item)
            await self.db.flush()

            # Insert new items
            for item in items_data:
                food = await self._find_food_by_name(item.food_name)
                food_id = food.id if food else None

                db_item = MealItem(
                    id=uuid.uuid4(),
                    meal_id=meal.id,
                    food_id=food_id,
                    food_name=item.food_name,
                    quantity=item.quantity,
                    unit=item.unit,
                    weight_grams=item.weight_grams,
                    calories=item.calories,
                    protein=item.protein,
                    carbs=item.carbs,
                    fat=item.fat,
                )
                self.db.add(db_item)
                if food_id:
                    await self._track_recent_food(user_id, food_id)

            await self.db.flush()

        # Reload updated meal representation
        ret_meal = await self.meal_repo.get_meal_with_items(meal_id)
        assert ret_meal is not None
        return ret_meal

    async def delete_meal(self, user_id: UUID, meal_id: UUID) -> bool:
        """Performs a soft delete on a logged meal."""
        meal = await self.meal_repo.get(meal_id)
        if not meal or meal.user_id != user_id or meal.deleted_at:
            return False

        meal.deleted_at = datetime.now(UTC)
        self.db.add(meal)
        await self.db.flush()
        return True

    async def get_meal_history(
        self, user_id: UUID, start_dt: datetime, end_dt: datetime
    ) -> list[Meal]:
        """Retrieves user's meal history logged within a range."""
        return await self.meal_repo.get_user_meals_in_range(user_id, start_dt, end_dt)

    async def get_daily_summary(
        self, user_id: UUID, target_date: date
    ) -> dict[str, Any]:
        """Aggregates consumed calories and macro values vs active goals for a date."""
        start_dt = datetime.combine(target_date, datetime.min.time(), tzinfo=UTC)
        end_dt = datetime.combine(target_date, datetime.max.time(), tzinfo=UTC)

        meals = await self.meal_repo.get_user_meals_in_range(user_id, start_dt, end_dt)

        consumed_cal = 0
        consumed_protein = 0.0
        consumed_carbs = 0.0
        consumed_fat = 0.0

        for meal in meals:
            for item in meal.items:
                consumed_cal += item.calories
                consumed_protein += float(item.protein)
                consumed_carbs += float(item.carbs)
                consumed_fat += float(item.fat)

        # Retrieve user active macro goals
        goal_stmt = select(UserGoal).filter(
            UserGoal.user_id == user_id, UserGoal.is_active.is_(True)
        )
        goal_res = await self.db.execute(goal_stmt)
        goal = goal_res.scalars().first()

        return {
            "date": target_date.isoformat(),
            "target_calories": goal.target_calories if goal else None,
            "consumed_calories": consumed_cal,
            "target_protein": (
                float(goal.target_protein) if goal and goal.target_protein else None
            ),
            "consumed_protein": round(consumed_protein, 1),
            "target_carbs": (
                float(goal.target_carbs) if goal and goal.target_carbs else None
            ),
            "consumed_carbs": round(consumed_carbs, 1),
            "target_fat": float(goal.target_fat) if goal and goal.target_fat else None,
            "consumed_fat": round(consumed_fat, 1),
        }

    async def get_weekly_summary(
        self, user_id: UUID, start_date: date
    ) -> dict[str, Any]:
        """Computes weekly totals, grouping calories/macros logged per day."""
        days_dict = {}
        total_cal = 0
        total_protein = 0.0
        total_carbs = 0.0
        total_fat = 0.0

        for idx in range(7):
            current_date = start_date + timedelta(days=idx)
            summary = await self.get_daily_summary(user_id, current_date)

            day_macros = DailyMacros(
                calories=summary["consumed_calories"],
                protein=summary["consumed_protein"],
                carbs=summary["consumed_carbs"],
                fat=summary["consumed_fat"],
            )
            days_dict[current_date.isoformat()] = day_macros

            total_cal += day_macros.calories
            total_protein += day_macros.protein
            total_carbs += day_macros.carbs
            total_fat += day_macros.fat

        avg_macros = DailyMacros(
            calories=int(total_cal / 7),
            protein=round(total_protein / 7, 1),
            carbs=round(total_carbs / 7, 1),
            fat=round(total_fat / 7, 1),
        )

        return {
            "start_date": start_date.isoformat(),
            "end_date": (start_date + timedelta(days=6)).isoformat(),
            "daily_average": avg_macros,
            "days": days_dict,
        }

    async def _find_food_by_name(self, name: str) -> Food | None:
        """Helper to find exact match food entries."""
        stmt = select(Food).filter(Food.name.ilike(name))
        res = await self.db.execute(stmt)
        return res.scalars().first()

    async def _track_recent_food(self, user_id: UUID, food_id: UUID) -> None:
        """Updates user recently logged foods list."""
        recent = await self.recent_repo.get_by_user_and_food(user_id, food_id)
        if recent:
            recent.last_used_at = datetime.now(UTC)
            self.db.add(recent)
        else:
            await self.recent_repo.create(
                {
                    "user_id": user_id,
                    "food_id": food_id,
                    "last_used_at": datetime.now(UTC),
                }
            )
