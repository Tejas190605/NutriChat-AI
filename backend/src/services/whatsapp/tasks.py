import asyncio
from typing import Any
from uuid import UUID

import structlog

from src.db.session import AsyncSessionLocal
from src.services.ai.meal_analyzer import MealAnalyzer
from src.services.ai.orchestrator import AIOrchestrator
from src.services.ai_service import AIConversationService
from src.services.celery_app import celery_app
from src.services.vision.pipeline import ImageUploadPipeline
from src.services.whatsapp.client import WhatsAppClient
from src.services.whatsapp.state_machine import ConversationStateMachine

logger = structlog.get_logger()


@celery_app.task(
    name="src.services.whatsapp.tasks.whatsapp_download_media_task",
    bind=True,
    max_retries=3,
)  # type: ignore[untyped-decorator]
def whatsapp_download_media_task(
    _self: Any, media_id: str, phone: str, user_id_str: str
) -> None:
    """Background task to download WhatsApp media, scan, upload, and trigger meal analysis."""
    logger.info("Executing Celery media download task", media_id=media_id, phone=phone)
    user_id = UUID(user_id_str)

    async def _download_and_process() -> None:
        async with AsyncSessionLocal() as session:
            client = WhatsAppClient()
            try:
                # 1. Download raw media bytes from Meta Graph API
                media_bytes = await client.download_media(media_id)

                # 2. Virus scanning abstraction (e.g., EICAR signature validation)
                if media_bytes.startswith(
                    b"X5O!P%@AP[4\\PZX54(P^)7CC)7}$EICAR-STANDARD-ANTIVIRUS-TEST-FILE!$H+H*"
                ):
                    logger.error(
                        "Malicious file signature detected in uploaded media stream!"
                    )
                    await client.send_text(
                        phone,
                        "⚠️ Media upload rejected: Security scanning flagged this file.",
                    )
                    return

                # 3. Process image upload via StorageProvider pipeline fallback
                upload_pipeline = ImageUploadPipeline(session)
                food_image = await upload_pipeline.upload_and_log(
                    user_id=user_id,
                    file_bytes=media_bytes,
                    _original_filename=f"wa_upload_{media_id[:8]}.jpg",
                )
                await session.commit()

                # 4. Trigger Meal Detections and OCR aggregates reasoning
                analyzer = MealAnalyzer(session)
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
                logger.error(
                    "Error executing background media download task", error=str(e)
                )
                await client.send_text(
                    phone,
                    "Sorry, I had trouble parsing that image log. Please try uploading again.",
                )
                raise e

    # Execute async loop block
    loop = asyncio.get_event_loop()
    loop.run_until_complete(_download_and_process())


@celery_app.task(
    name="src.services.whatsapp.tasks.whatsapp_process_incoming_task"
)  # type: ignore[untyped-decorator]
def whatsapp_process_incoming_task(phone: str, message_text: str) -> None:
    """Orchestrates state machine onboarding steps and conversational coaching logs."""
    logger.info(
        "Executing Celery incoming message routing task",
        phone=phone,
        message=message_text,
    )

    async def _process_incoming() -> None:
        async with AsyncSessionLocal() as session:
            client = WhatsAppClient()
            state_machine = ConversationStateMachine(session, phone)

            # 1. Run onboarding or reset state cycle
            reply_text, onboarding_completed = await state_machine.run_state_cycle(
                message_text
            )
            if reply_text:
                await client.send_text(phone, reply_text)
                return

            # 2. Returning User Flow: Routing queries to AI orchestrator
            user = await state_machine.lookup_user()
            if user:
                # Find or start conversation session thread
                conv_service = AIConversationService(session)
                conversations = await conv_service.get_user_conversations(user.id)

                if conversations:
                    conv = conversations[0]
                else:
                    conv = await conv_service.start_conversation(
                        user_id=user.id, title="WhatsApp Session Chat"
                    )
                    await session.commit()

                # Process message via AIOrchestrator
                orchestrator = AIOrchestrator(session)
                reply = await orchestrator.process_chat_message(
                    user_id=user.id,
                    conversation_id=conv.id,
                    user_message=message_text,
                )
                await client.send_text(phone, reply)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(_process_incoming())
