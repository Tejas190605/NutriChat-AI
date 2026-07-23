from typing import Any

import httpx
import structlog

from src.config.settings import settings

logger = structlog.get_logger()


class WhatsAppClient:
    """Meta Cloud API HTTP client wrapper for messaging and media retrieval."""

    def __init__(self) -> None:
        self.phone_number_id = settings.WHATSAPP_PHONE_NUMBER_ID
        self.access_token = settings.WHATSAPP_ACCESS_TOKEN
        self.is_mock = self.access_token == "dev_whatsapp_access_token"

        self.base_url = f"https://graph.facebook.com/v20.0/{self.phone_number_id}"
        self.headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
        }

    async def _send_raw_message(self, payload: dict[str, Any]) -> dict[str, Any]:
        """Submits message request payload to Meta APIs."""
        if self.is_mock:
            logger.info("WhatsApp send message (MOCK)", payload=payload)
            return {
                "messaging_product": "whatsapp",
                "contacts": [{"input": payload.get("to")}],
                "messages": [{"id": "wamid.HBgL"}],
            }

        async with httpx.AsyncClient() as client:
            resp = await client.post(
                f"{self.base_url}/messages",
                json=payload,
                headers=self.headers,
                timeout=15.0,
            )
            resp.raise_for_status()
            return dict(resp.json())

    async def send_text(self, to: str, text: str) -> dict[str, Any]:
        """Sends simple plaintext WhatsApp message."""
        payload = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": to,
            "type": "text",
            "text": {"preview_url": False, "body": text},
        }
        return await self._send_raw_message(payload)

    async def send_image(
        self, to: str, image_url: str, caption: str | None = None
    ) -> dict[str, Any]:
        """Sends image URL message."""
        payload = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": to,
            "type": "image",
            "image": {"link": image_url},
        }
        if caption:
            payload["image"]["caption"] = caption  # type: ignore
        return await self._send_raw_message(payload)

    async def send_buttons(
        self, to: str, text: str, buttons: list[dict[str, str]]
    ) -> dict[str, Any]:
        """Sends quick reply interactive buttons message."""
        # Max 3 buttons supported by Meta
        formatted_buttons = []
        for btn in buttons[:3]:
            formatted_buttons.append(
                {
                    "type": "reply",
                    "reply": {"id": btn["id"], "title": btn["title"]},
                }
            )

        payload = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": to,
            "type": "interactive",
            "interactive": {
                "type": "button",
                "body": {"text": text},
                "action": {"buttons": formatted_buttons},
            },
        }
        return await self._send_raw_message(payload)

    async def send_list(
        self, to: str, text: str, button_title: str, sections: list[dict[str, Any]]
    ) -> dict[str, Any]:
        """Sends interactive select list menu option."""
        payload = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": to,
            "type": "interactive",
            "interactive": {
                "type": "list",
                "body": {"text": text},
                "action": {"button": button_title, "sections": sections},
            },
        }
        return await self._send_raw_message(payload)

    async def send_typing_indicator(self, to: str, state: str = "typing") -> None:
        """Sends typing indicators status or marks message as read."""
        if self.is_mock:
            logger.info("WhatsApp typing indicator status", to=to, state=state)
            return

        # Meta message read confirmation status payload
        # Note: WhatsApp Cloud API typing indicators are simulated by marking chat messages as read
        payload = {"messaging_product": "whatsapp", "status": "read", "message_id": to}
        try:
            async with httpx.AsyncClient() as client:
                await client.post(
                    f"{self.base_url}/messages",
                    json=payload,
                    headers=self.headers,
                    timeout=5.0,
                )
        except Exception as e:
            logger.warning(
                "Failed to send read status confirmation indicator to WhatsApp API",
                error=str(e),
            )

    async def download_media(self, media_id: str) -> bytes:
        """Retrieves and downloads raw binary payload for a WhatsApp media ID."""
        if self.is_mock:
            logger.info("WhatsApp download media (MOCK)", media_id=media_id)
            # Return a simple 1x1 mock transparent pixel gif as fallback mock media bytes
            return b"GIF89a\x01\x00\x01\x00\x80\x00\x00\xff\xff\xff\x00\x00\x00!\xf9\x04\x01\x00\x00\x00\x00,\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02D\x01\x00;"

        async with httpx.AsyncClient() as client:
            # 1. Fetch download url path from media object ID
            media_info_url = f"https://graph.facebook.com/v20.0/{media_id}"
            headers = {"Authorization": f"Bearer {self.access_token}"}

            resp = await client.get(media_info_url, headers=headers, timeout=15.0)
            resp.raise_for_status()
            download_url = resp.json().get("url")

            if not download_url:
                raise ValueError(
                    f"Download URL not found in metadata response for media_id: {media_id}"
                )

            # 2. Fetch binary stream
            media_binary_resp = await client.get(
                download_url, headers=headers, timeout=30.0
            )
            media_binary_resp.raise_for_status()
            return media_binary_resp.content
