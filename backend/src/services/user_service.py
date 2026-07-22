from datetime import UTC, date, datetime
from uuid import UUID

import structlog
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.activity import ActivityLevel
from src.models.goal import UserGoal
from src.models.profile import UserProfile
from src.models.user import User
from src.models.weight import WeightHistory
from src.repositories.base import BaseRepository
from src.schemas.profile import UserProfileUpdateRequest

logger = structlog.get_logger()


class UserService:
    """Business service driving user profiles, health goals, and weight logging."""

    def __init__(self, db: AsyncSession):
        self.db = db
        self.user_repo = BaseRepository(User, db)
        self.profile_repo = BaseRepository(UserProfile, db)
        self.goal_repo = BaseRepository(UserGoal, db)
        self.weight_repo = BaseRepository(WeightHistory, db)
        self.activity_repo = BaseRepository(ActivityLevel, db)

    async def get_profile(self, user_id: UUID) -> UserProfile:
        """Retrieves a user's profile entity, creating one if not initialized."""
        query = select(UserProfile).filter(UserProfile.user_id == user_id)
        result = await self.db.execute(query)
        profile = result.scalars().first()

        if not profile:
            # Initialize empty profile boilerplate
            profile = await self.profile_repo.create(
                {
                    "user_id": user_id,
                    "first_name": None,
                    "last_name": None,
                    "phone_number": None,
                    "gender": None,
                    "date_of_birth": None,
                    "height": None,
                    "weight": None,
                }
            )
        return profile

    async def update_profile(
        self, user_id: UUID, data: UserProfileUpdateRequest
    ) -> UserProfile:
        """Updates a user's profile details in the database."""
        profile = await self.get_profile(user_id)
        assert profile is not None  # get_profile guarantees creation

        update_data = data.model_dump(exclude_unset=True)
        updated_profile = await self.profile_repo.update(profile, update_data)

        # If weight is updated, log it in the weight history too
        if "weight" in update_data and update_data["weight"] is not None:
            await self.log_weight(user_id, float(update_data["weight"]))

        return updated_profile

    async def log_weight(self, user_id: UUID, weight: float) -> WeightHistory:
        """Logs a weight entry in history and updates current weight in profile."""
        log = await self.weight_repo.create(
            {
                "user_id": user_id,
                "weight": weight,
                "logged_at": datetime.now(UTC),
            }
        )

        # Update current weight on profile
        query = select(UserProfile).filter(UserProfile.user_id == user_id)
        result = await self.db.execute(query)
        profile = result.scalars().first()
        if profile and profile.weight != weight:
            profile.weight = weight
            self.db.add(profile)

        return log

    async def get_weight_history(self, user_id: UUID) -> list[WeightHistory]:
        """Retrieves a user's chronological weight history logs."""
        query = (
            select(WeightHistory)
            .filter(WeightHistory.user_id == user_id)
            .order_by(WeightHistory.logged_at.desc())
        )
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def calculate_and_save_goals(
        self, user_id: UUID, goal_type: str, activity_multiplier: float = 1.2
    ) -> UserGoal:
        """Calculates TDEE and macro splits using Mifflin-St Jeor, saving as active goal."""
        profile = await self.get_profile(user_id)

        # Fallback defaults if profile variables are not complete yet
        height = float(profile.height) if profile.height else 170.0
        weight = float(profile.weight) if profile.weight else 70.0
        gender = profile.gender.lower() if profile.gender else "male"

        # Calculate age
        age = 25
        if profile.date_of_birth:
            dob = profile.date_of_birth
            today = date.today()
            age = (
                today.year
                - dob.year
                - ((today.month, today.day) < (dob.month, dob.day))
            )

        # Mifflin-St Jeor Equation
        if gender == "female":
            bmr = (10 * weight) + (6.25 * height) - (5 * age) - 161
        else:
            bmr = (10 * weight) + (6.25 * height) - (5 * age) + 5

        tdee = bmr * activity_multiplier

        # Apply goal adjustments
        if goal_type == "weight_loss":
            target_calories = int(tdee - 500)
        elif goal_type == "muscle_gain":
            target_calories = int(tdee + 300)
        else:  # maintenance
            target_calories = int(tdee)

        # Enforce health floor calories (never log below 1200 kcal)
        if target_calories < 1200:
            target_calories = 1200

        # Macronutrient split ratios:
        # Protein: 2.0g per kg body weight
        protein_grams = weight * 2.0
        protein_kcal = protein_grams * 4

        # Fat: 25% of daily target calories
        fat_kcal = target_calories * 0.25
        fat_grams = fat_kcal / 9

        # Carbs: Remaining calories
        carbs_kcal = target_calories - (protein_kcal + fat_kcal)
        if carbs_kcal < 0:
            carbs_kcal = 0
        carbs_grams = carbs_kcal / 4

        # Deactivate old goals
        await self.db.execute(
            update(UserGoal).filter(UserGoal.user_id == user_id).values(is_active=False)
        )

        # Create new active goal record
        goal = await self.goal_repo.create(
            {
                "user_id": user_id,
                "goal_type": goal_type,
                "target_weight": profile.weight,
                "target_calories": target_calories,
                "target_protein": round(protein_grams, 1),
                "target_carbs": round(carbs_grams, 1),
                "target_fat": round(fat_grams, 1),
                "is_active": True,
            }
        )

        return goal

    async def get_active_goal(self, user_id: UUID) -> UserGoal | None:
        """Retrieves a user's currently active fitness/macro goal."""
        query = select(UserGoal).filter(
            UserGoal.user_id == user_id, UserGoal.is_active.is_(True)
        )
        result = await self.db.execute(query)
        return result.scalars().first()
