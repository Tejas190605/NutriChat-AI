import json
from datetime import date
from typing import Any
from uuid import uuid4

import structlog
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.profile import UserProfile
from src.models.user import User
from src.services.auth_service import AuthService
from src.services.redis_client import get_redis_client
from src.services.user_service import UserService
from src.services.whatsapp.client import WhatsAppClient

logger = structlog.get_logger()


class ConversationStateMachine:
    """State machine executing user registration and profile parameters onboarding via WhatsApp."""

    def __init__(self, db: AsyncSession, phone: str) -> None:
        self.db = db
        self.phone = phone
        self.redis_key = f"whatsapp_session:{phone}"
        self.client = WhatsAppClient()
        self.user_service = UserService(db)
        self.auth_service = AuthService(db)
        self.redis = get_redis_client()

    async def get_session_data(self) -> dict[str, Any] | None:
        """Retrieves user onboarding metrics stored inside Redis cache."""
        data = await self.redis.get(self.redis_key)
        if not data:
            return None
        return dict(json.loads(data))

    async def save_session_data(self, data: dict[str, Any], ttl: int = 86400) -> None:
        """Saves current state metrics to Redis cache with auto-expiration."""
        await self.redis.set(self.redis_key, json.dumps(data), ex=ttl)

    async def clear_session(self) -> None:
        """Removes session keys from Redis cache."""
        await self.redis.delete(self.redis_key)

    async def lookup_user(self) -> User | None:
        """Checks if a user profile already exists with the sender's phone number."""
        stmt = select(UserProfile).filter(UserProfile.phone_number == self.phone)
        res = await self.db.execute(stmt)
        profile = res.scalars().first()
        if profile:
            # Load user relation
            stmt_user = select(User).filter(User.id == profile.user_id)
            res_user = await self.db.execute(stmt_user)
            return res_user.scalars().first()
        return None

    async def run_state_cycle(self, incoming_text: str) -> tuple[str, bool]:
        """Runs state transition operations based on incoming message content.

        Args:
            incoming_text: Cleaned body query from user.

        Returns:
            A tuple containing (reply_text, onboarding_completed).
        """
        # 1. Reset check
        if incoming_text.strip().lower() == "/reset":
            await self.clear_session()
            session = None
        else:
            session = await self.get_session_data()

        # 2. Returning User check
        user = await self.lookup_user()
        if user and not session:
            # User is logged in and not in onboarding state
            return "", False

        # 3. Initialize session if not present
        if not session:
            session = {
                "state": "WELCOME",
                "phone": self.phone,
                "data": {},
            }
            await self.save_session_data(session)

        state = session["state"]
        data = session["data"]

        # 4. State handlers
        if state == "WELCOME":
            session["state"] = "ONBOARDING_NAME"
            await self.save_session_data(session)
            reply = (
                "Welcome to NutriChat AI! 🥦\n"
                "I am your autonomous nutrition coach. Let's set up your profile.\n\n"
                "To start, what is your first name?"
            )
            return reply, False

        elif state == "ONBOARDING_NAME":
            name = incoming_text.strip()
            if not name or len(name) < 2:
                return (
                    "Please enter a valid name (at least 2 letters long). What is your first name?",
                    False,
                )

            data["first_name"] = name
            session["state"] = "ONBOARDING_AGE"
            await self.save_session_data(session)
            return (
                f"Nice to meet you, {name}! How old are you? (Enter age in years, e.g. 28)",
                False,
            )

        elif state == "ONBOARDING_AGE":
            try:
                age = int(incoming_text.strip())
                if age < 10 or age > 100:
                    raise ValueError()
            except ValueError:
                return (
                    "Please enter a valid age between 10 and 100. How old are you?",
                    False,
                )

            data["age"] = age
            session["state"] = "ONBOARDING_GENDER"
            await self.save_session_data(session)

            # Send buttons if possible, else return plain text choices
            buttons = [
                {"id": "male", "title": "Male"},
                {"id": "female", "title": "Female"},
                {"id": "other", "title": "Other"},
            ]
            await self.client.send_buttons(self.phone, "What is your gender?", buttons)
            return "Please select or type your gender (Male, Female, Other):", False

        elif state == "ONBOARDING_GENDER":
            gender = incoming_text.strip().lower()
            if gender not in ["male", "female", "other"]:
                return (
                    "Please select one of the gender options (Male, Female, Other):",
                    False,
                )

            data["gender"] = gender
            session["state"] = "ONBOARDING_HEIGHT"
            await self.save_session_data(session)
            return "What is your height in centimeters? (e.g. 175)", False

        elif state == "ONBOARDING_HEIGHT":
            try:
                height = float(incoming_text.strip())
                if height < 100 or height > 250:
                    raise ValueError()
            except ValueError:
                return (
                    "Please enter a valid height between 100cm and 250cm. What is your height?",
                    False,
                )

            data["height"] = height
            session["state"] = "ONBOARDING_WEIGHT"
            await self.save_session_data(session)
            return "What is your current weight in kilograms? (e.g. 72.5)", False

        elif state == "ONBOARDING_WEIGHT":
            try:
                weight = float(incoming_text.strip())
                if weight < 30 or weight > 200:
                    raise ValueError()
            except ValueError:
                return (
                    "Please enter a valid weight between 30kg and 200kg. What is your weight?",
                    False,
                )

            data["weight"] = weight
            session["state"] = "ONBOARDING_ACTIVITY"
            await self.save_session_data(session)

            buttons = [
                {"id": "sedentary", "title": "Sedentary"},
                {"id": "active", "title": "Active"},
                {"id": "very_active", "title": "Very Active"},
            ]
            await self.client.send_buttons(
                self.phone, "What is your daily physical activity level?", buttons
            )
            return "Enter activity level (Sedentary, Active, Very Active):", False

        elif state == "ONBOARDING_ACTIVITY":
            activity_input = incoming_text.strip().lower()
            multipliers = {
                "sedentary": 1.2,
                "active": 1.55,
                "very_active": 1.725,
            }
            if activity_input not in multipliers:
                return (
                    "Please select a valid activity level (Sedentary, Active, Very Active):",
                    False,
                )

            data["activity_multiplier"] = multipliers[activity_input]
            session["state"] = "ONBOARDING_GOAL"
            await self.save_session_data(session)

            buttons = [
                {"id": "weight_loss", "title": "Weight Loss"},
                {"id": "weight_gain", "title": "Weight Gain"},
                {"id": "maintenance", "title": "Maintenance"},
            ]
            await self.client.send_buttons(
                self.phone, "What is your target fitness goal?", buttons
            )
            return "Enter target goal (Weight Loss, Weight Gain, Maintenance):", False

        elif state == "ONBOARDING_GOAL":
            goal_input = incoming_text.strip().lower()
            goals_map = {
                "weight_loss": "weight_loss",
                "weight loss": "weight_loss",
                "weight_gain": "muscle_gain",
                "weight gain": "muscle_gain",
                "muscle_gain": "muscle_gain",
                "muscle gain": "muscle_gain",
                "maintenance": "maintenance",
                "weight_maintenance": "maintenance",
            }
            if goal_input not in goals_map:
                return (
                    "Please select a valid fitness goal (Weight Loss, Weight Gain, Maintenance):",
                    False,
                )

            target_goal = goals_map[goal_input]

            # 5. Onboarding complete! Create user records in Postgres DB
            logger.info(
                "Onboarding completed successfully. Registering user profile.",
                data=data,
            )

            # Generate placeholder user credentials for WhatsApp user
            email = f"wa_{self.phone.replace('+', '')}@whatsapp.nutrichat.ai"
            password = f"secret_wa_pass_{uuid4().hex}"

            try:
                # Register user
                user_obj = await self.auth_service.register_user(email, password)

                # Fetch profile and save parsed onboarding details
                profile_obj = await self.user_service.get_profile(user_obj.id)
                profile_obj.first_name = data["first_name"]
                profile_obj.phone_number = self.phone
                profile_obj.gender = data["gender"]
                profile_obj.height = data["height"]
                profile_obj.weight = data["weight"]

                # Deduce approximate DOB based on age
                dob_year = date.today().year - data["age"]
                profile_obj.date_of_birth = date(dob_year, 1, 1)

                self.db.add(profile_obj)
                await self.db.commit()

                # Calculate calories and macro targets splits
                goal_obj = await self.user_service.calculate_and_save_goals(
                    user_id=user_obj.id,
                    goal_type=target_goal,
                    activity_multiplier=data["activity_multiplier"],
                )
                await self.db.commit()

                # Log weight to history
                await self.user_service.log_weight(user_obj.id, data["weight"])
                await self.db.commit()

                # Onboarding success response message
                reply = (
                    f"Profile setup completed! 🎉\n\n"
                    f"Calories target: *{goal_obj.target_calories} kcal*\n"
                    f"Protein target: *{goal_obj.target_protein}g*\n"
                    f"Carbs target: *{goal_obj.target_carbs}g*\n"
                    f"Fat target: *{goal_obj.target_fat}g*\n\n"
                    "You are now ready to log meals! Simply send a photo of your food, a barcode, "
                    "or description text to begin tracking."
                )

                await self.clear_session()
                return reply, True

            except Exception as e:
                logger.error(
                    "Failed to commit onboarding user profile to database", error=str(e)
                )
                await self.db.rollback()
                return (
                    "I encountered a registration error saving your profile details. Please send /reset to restart.",
                    False,
                )

        return "Please send /reset to restart onboarding configurations.", False
