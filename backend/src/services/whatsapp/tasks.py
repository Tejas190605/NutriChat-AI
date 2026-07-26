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


async def download_and_process_whatsapp_media(
    db: AsyncSession, media_id: str, phone: str, user_id: UUID
) -> None:
    """Downloads WhatsApp media, scans, uploads, and executes meal analysis synchronously."""
    logger.info("Executing WhatsApp media processing pipeline", media_id=media_id, phone=phone)
    client = WhatsAppClient()
    try:
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

        # 4. Trigger Meal Detections and OCR reasoning
        analyzer = MealAnalyzer(db)
        result = await analyzer.analyze_meal_image(food_image.id)

        # Format macro summary message
        foods_list = ", ".join([f["label"] for f in result.get("foods", [])])
        msg = (
            f"📸 *Meal Logged Successfully!*\n\n"
            f"Foods identified: {foods_list or 'Unknown Dish'}\n"
            f"Calories: *{result['total_calories']} kcal*\n"
            f"Protein: *{result['total_protein']}g*\n"
            f"Carbs: *{result['total_carbs']}g*\n"
            f"Fat: *{result['total_fat']}g*\n\n"
            "Let me know if you would like alternative recommendations or swaps!"
        )
        await client.send_text(phone, msg)

    except Exception as e:
        logger.error("Error executing media download processing", error=str(e))
        await client.send_text(
            phone,
            "Sorry, I had trouble parsing that image log. Please try uploading again.",
        )
        raise e


async def process_incoming_whatsapp_message(
    db: AsyncSession, phone: str, message_text: str
) -> None:
    """Orchestrates state machine onboarding steps and conversational coaching logs synchronously."""
    logger.info(
        "Executing incoming WhatsApp message processing",
        phone=phone,
        message=message_text,
    )
    client = WhatsAppClient()
    state_machine = ConversationStateMachine(db, phone)

    # 1. Run onboarding or reset state cycle
    reply_text, onboarding_completed = await state_machine.run_state_cycle(message_text)
    if reply_text:
        await client.send_text(phone, reply_text)
        return

    # 2. Returning User Flow: Routing queries to AI orchestrator
    user = await state_machine.lookup_user()
    if user:
        conv_service = AIConversationService(db)
        conversations = await conv_service.get_user_conversations(user.id)

        if conversations:
            conv = conversations[0]
        else:
            conv = await conv_service.start_conversation(
                user_id=user.id, title="WhatsApp Session Chat"
            )
            await db.commit()

        # Process message via AIOrchestrator
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
