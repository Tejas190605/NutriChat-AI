from uuid import UUID

import structlog
from sqlalchemy.ext.asyncio import AsyncSession

from src.services.ai.meal_analyzer import MealAnalyzer
from src.services.ai.orchestrator import AIOrchestrator
from src.services.ai_service import AIConversationService
from src.services.vision.pipeline import ImageUploadPipeline
from src.services.whatsapp.client import WhatsAppClient
from src.services.whatsapp.state_machine import ConversationStateMachine

logger = structlog.get_logger()


from datetime import UTC, date, datetime
from uuid import UUID, uuid4

import structlog
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.user import User
from src.schemas.meal import MealItemCreate
from src.services.ai.meal_analyzer import MealAnalyzer
from src.services.ai.orchestrator import AIOrchestrator
from src.services.ai_service import AIConversationService
from src.services.auth_service import AuthService
from src.services.meal_service import MealService
from src.services.user_service import UserService
from src.services.vision.pipeline import ImageUploadPipeline
from src.services.whatsapp.client import WhatsAppClient
from src.services.whatsapp.state_machine import ConversationStateMachine

logger = structlog.get_logger()


async def get_or_create_whatsapp_user(db: AsyncSession, phone: str) -> User:
    """Retrieves existing user profile matching phone number or creates a lightweight WhatsApp user."""
    state_machine = ConversationStateMachine(db, phone)
    user = await state_machine.lookup_user()
    if user:
        return user

    clean_phone = phone.replace("+", "").replace(" ", "").replace("-", "")
    email = f"wa_{clean_phone}@whatsapp.nutrichat.ai"
    password = f"secret_wa_pass_{uuid4().hex}"

    auth_service = AuthService(db)
    user_service = UserService(db)

    try:
        user_obj = await auth_service.register_user(email, password)
        profile_obj = await user_service.get_profile(user_obj.id)
        profile_obj.first_name = "WhatsApp User"
        profile_obj.phone_number = phone
        db.add(profile_obj)
        await db.commit()

        await user_service.calculate_and_save_goals(
            user_id=user_obj.id,
            goal_type="maintenance",
            activity_multiplier=1.2,
        )
        await db.commit()
        return user_obj
    except Exception as e:
        logger.warning("Error creating lightweight WhatsApp user, retrieving existing or retrying", error=str(e))
        await db.rollback()
        existing = await state_machine.lookup_user()
        if existing:
            return existing
        raise e


async def download_and_process_whatsapp_media(
    db: AsyncSession, media_id: str, phone: str, user_id: UUID | None = None
) -> None:
    """Downloads WhatsApp media, scans, uploads, executes AI meal analysis, persists meal to DB, and sends WhatsApp response."""
    logger.info("Executing WhatsApp media processing pipeline", media_id=media_id, phone=phone)
    client = WhatsAppClient()
    try:
        # 0. Ensure user entity is resolved
        if not user_id:
            user = await get_or_create_whatsapp_user(db, phone)
            user_id = user.id

        # 1. Download raw media bytes from Meta Graph API
        media_bytes = await client.download_media(media_id)

        # 2. Virus scanning check (e.g., EICAR signature validation)
        if media_bytes.startswith(
            b"X5O!P%@AP[4\\PZX54(P^)7CC)7}$EICAR-STANDARD-ANTIVIRUS-TEST-FILE!$H+H*"
        ):
            logger.error("Malicious file signature detected in uploaded media stream!")
            await client.send_text(
                phone,
                "⚠️ Media upload rejected: Security scanning flagged this file.",
            )
            return

        # 3. Process image upload via StorageProvider pipeline
        upload_pipeline = ImageUploadPipeline(db)
        food_image = await upload_pipeline.upload_and_log(
            user_id=user_id,
            file_bytes=media_bytes,
            _original_filename=f"wa_upload_{media_id[:8]}.jpg",
        )
        await db.commit()

        # 4. Trigger Meal Detections and Gemini AI analysis
        analyzer = MealAnalyzer(db)
        result = await analyzer.analyze_meal_image(food_image.id)

        # 5. Build MealItem models and persist to PostgreSQL via MealService
        items_create: list[MealItemCreate] = []
        raw_foods = result.get("foods", [])
        total_cals = result.get("total_calories", 0)

        if raw_foods:
            for food in raw_foods:
                item_cals = food.get("calories", 0)
                ratio = item_cals / max(total_cals, 1)
                items_create.append(
                    MealItemCreate(
                        food_name=food.get("label", "Analyzed Food"),
                        quantity=1.0,
                        unit=food.get("portion", "serving"),
                        weight_grams=food.get("weight_grams", 200.0),
                        calories=item_cals,
                        protein=round(result.get("total_protein", 0.0) * ratio, 1),
                        carbs=round(result.get("total_carbs", 0.0) * ratio, 1),
                        fat=round(result.get("total_fat", 0.0) * ratio, 1),
                    )
                )
        else:
            items_create.append(
                MealItemCreate(
                    food_name="Analyzed Meal",
                    quantity=1.0,
                    unit="serving",
                    weight_grams=200.0,
                    calories=total_cals,
                    protein=result.get("total_protein", 0.0),
                    carbs=result.get("total_carbs", 0.0),
                    fat=result.get("total_fat", 0.0),
                )
            )

        meal_service = MealService(db)
        primary_name = items_create[0].food_name if items_create else "WhatsApp Meal"
        await meal_service.log_meal(
            user_id=user_id,
            name=primary_name,
            items_data=items_create,
            image_url=food_image.image_url,
        )
        await db.commit()

        # 6. Fetch today's updated daily totals
        daily_summary = await meal_service.get_daily_summary(user_id, date.today())

        consumed_cal = daily_summary.get("consumed_calories", total_cals)
        target_cal = daily_summary.get("target_calories") or 1800
        foods_label = ", ".join([item.food_name for item in items_create])

        # 7. Construct and send WhatsApp response message
        msg = (
            f"🥗 *Meal Analyzed*\n\n"
            f"*{foods_label}*\n\n"
            f"🔥 Calories: *{total_cals} kcal*\n"
            f"🥩 Protein: *{result.get('total_protein', 0)} g*\n"
            f"🍚 Carbs: *{result.get('total_carbs', 0)} g*\n"
            f"🥑 Fat: *{result.get('total_fat', 0)} g*\n"
            f"🌾 Fiber: *{result.get('fiber_g', 0)} g*\n\n"
            f"📊 *Today's Calories*\n"
            f"{consumed_cal} / {target_cal} kcal\n\n"
            f"✅ Meal saved to your NutriChat diary.\n\n"
            f"💡 Tip: {result.get('reasoning') or 'Great job tracking your nutrition!'}\n\n"
            f"⚠️ Nutrition values are AI estimates and may vary with ingredients and portion size."
        )
        await client.send_text(phone, msg)

    except Exception as e:
        logger.error("Error executing media download processing", error=str(e))
        await client.send_text(
            phone,
            "Sorry, I had trouble parsing that image. Please try sending your meal photo again.",
        )
        raise e


async def process_incoming_whatsapp_message(
    db: AsyncSession, phone: str, message_text: str
) -> None:
    """Orchestrates WhatsApp text commands, state machine onboarding, and AI coaching response."""
    logger.info(
        "Executing incoming WhatsApp message processing",
        phone=phone,
        message=message_text,
    )
    client = WhatsAppClient()
    clean_text = message_text.strip().lower()

    # 1. Quick WhatsApp Command Handlers
    if clean_text in ["hello", "hi", "help", "/help"]:
        help_msg = (
            "👋 Hi! I'm NutriChat AI.\n\n"
            "Send me a photo of your meal and I'll estimate its calories and nutritional information.\n\n"
            "You can also send:\n"
            "• *today* - View today's total calories & macros\n"
            "• *history* - View recent meals logged today\n"
            "• *help* - View this help menu"
        )
        await client.send_text(phone, help_msg)
        return

    if clean_text == "today":
        user = await get_or_create_whatsapp_user(db, phone)
        meal_service = MealService(db)
        summary = await meal_service.get_daily_summary(user.id, date.today())

        consumed_cal = summary.get("consumed_calories", 0)
        target_cal = summary.get("target_calories") or 1800
        consumed_p = summary.get("consumed_protein", 0.0)
        target_p = summary.get("target_protein") or 90.0
        consumed_c = summary.get("consumed_carbs", 0.0)
        target_c = summary.get("target_carbs") or 220.0
        consumed_f = summary.get("consumed_fat", 0.0)
        target_f = summary.get("target_fat") or 60.0

        today_msg = (
            "📊 *Today's Nutrition Summary*\n\n"
            f"🔥 Calories: *{consumed_cal} / {target_cal} kcal*\n"
            f"🥩 Protein: *{consumed_p} / {target_p} g*\n"
            f"🍚 Carbs: *{consumed_c} / {target_c} g*\n"
            f"🥑 Fat: *{consumed_f} / {target_f} g*"
        )
        await client.send_text(phone, today_msg)
        return

    if clean_text == "history":
        user = await get_or_create_whatsapp_user(db, phone)
        meal_service = MealService(db)
        today = date.today()
        start_dt = datetime.combine(today, datetime.min.time(), tzinfo=UTC)
        end_dt = datetime.combine(today, datetime.max.time(), tzinfo=UTC)

        meals = await meal_service.get_meal_history(user.id, start_dt, end_dt)
        if not meals:
            await client.send_text(
                phone,
                "🍽 *Today's Meals*\n\nNo meals logged today yet. Send a food photo to start tracking!",
            )
            return

        lines = ["🍽 *Today's Meals*\n"]
        total_cals = 0
        for meal in meals:
            m_cals = sum(item.calories for item in meal.items)
            total_cals += m_cals
            lines.append(f"• {meal.name} — *{m_cals} kcal*")
        lines.append(f"\nTotal: *{total_cals} kcal*")
        await client.send_text(phone, "\n".join(lines))
        return

    # 2. Onboarding state machine check
    state_machine = ConversationStateMachine(db, phone)
    reply_text, onboarding_completed = await state_machine.run_state_cycle(message_text)
    if reply_text:
        await client.send_text(phone, reply_text)
        return

    # 3. Returning User Flow: Routing queries to AI orchestrator
    user = await state_machine.lookup_user()
    if not user:
        user = await get_or_create_whatsapp_user(db, phone)

    conv_service = AIConversationService(db)
    conversations = await conv_service.get_user_conversations(user.id)

    if conversations:
        conv = conversations[0]
    else:
        conv = await conv_service.start_conversation(
            user_id=user.id, title="WhatsApp Session Chat"
        )
        await db.commit()

    orchestrator = AIOrchestrator(db)
    reply = await orchestrator.process_chat_message(
        user_id=user.id,
        conversation_id=conv.id,
        user_message=message_text,
    )
    await client.send_text(phone, reply)


# Backward compatibility aliases
whatsapp_download_media_task = download_and_process_whatsapp_media
whatsapp_process_incoming_task = process_incoming_whatsapp_message

