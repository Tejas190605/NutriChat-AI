from typing import Any

import structlog
from sqlalchemy.ext.asyncio import AsyncSession

from src.services.redis_client import get_redis_client
from src.services.whatsapp.state_machine import ConversationStateMachine
from src.services.whatsapp.tasks import (
    download_and_process_whatsapp_media,
    process_incoming_whatsapp_message,
)

logger = structlog.get_logger()


class WhatsAppRouter:
    """Decodes Meta payloads, checks duplicate locks, and routes requests synchronously."""

    def __init__(self, db: AsyncSession) -> None:
        self.db = db
        self.redis = get_redis_client()

    async def route_payload(self, body: dict[str, Any]) -> None:
        """Parses webhook schema models and dispatches jobs directly.

        Args:
            body: Raw JSON payload dictionary from Meta.
        """
        # 1. Parse Meta Cloud API entry blocks
        entries = body.get("entry", [])
        if not entries:
            return

        for entry in entries:
            changes = entry.get("changes", [])
            for change in changes:
                value = change.get("value", {})
                messages = value.get("messages", [])

                for msg in messages:
                    msg_id = msg.get("id")
                    from_phone = msg.get("from")

                    # 2. Replay protection & message deduplication
                    if msg_id:
                        lock_key = f"whatsapp_msg_lock:{msg_id}"
                        # Try to set Redis key (lock TTL: 5 minutes)
                        is_new = await self.redis.set(lock_key, "1", ex=300, nx=True)
                        if not is_new:
                            logger.info(
                                "Discarding duplicate WhatsApp webhook message payload",
                                message_id=msg_id,
                            )
                            continue

                    # 3. Detect payload content type
                    msg_type = msg.get("type")

                    # Onboarding State Machine check
                    state_machine = ConversationStateMachine(self.db, from_phone)
                    user = await state_machine.lookup_user()

                    # Retrieve text representation
                    text_content = ""
                    if msg_type == "text":
                        text_content = msg.get("text", {}).get("body", "")
                    elif msg_type == "interactive":
                        interactive_type = msg.get("interactive", {}).get("type")
                        if interactive_type == "button_reply":
                            text_content = (
                                msg.get("interactive", {})
                                .get("button_reply", {})
                                .get("title", "")
                            )
                        elif interactive_type == "list_reply":
                            text_content = (
                                msg.get("interactive", {})
                                .get("list_reply", {})
                                .get("title", "")
                            )

                    # Route reset commands immediately
                    if text_content.strip().lower() == "/reset":
                        await process_incoming_whatsapp_message(
                            self.db, from_phone, "/reset"
                        )
                        continue

                    # 4. Handle Media/Image intakes
                    if msg_type == "image":
                        image_id = msg.get("image", {}).get("id")
                        user_id = user.id if user else None

                        if image_id:
                            # Execute media download & food analysis pipeline
                            await download_and_process_whatsapp_media(
                                db=self.db,
                                media_id=image_id,
                                phone=from_phone,
                                user_id=user_id,
                            )
                        continue

                    # 5. Route Onboarding state replies or standard chat text
                    if text_content:
                        await process_incoming_whatsapp_message(
                            self.db, from_phone, text_content
                        )
                    else:
                        logger.warning(
                            "Unsupported WhatsApp message format type received",
                            type=msg_type,
                        )
