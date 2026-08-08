from typing import Any

import httpx
import structlog

from src.config.settings import settings

logger = structlog.get_logger()


class WhatsAppClient:
    """Meta Cloud API HTTP client wrapper for messaging and media retrieval."""

    def __init__(self) -> None:
        self.phone_number_id = (settings.WHATSAPP_PHONE_NUMBER_ID or "").strip().strip('"').strip("'")
        raw_token = (settings.WHATSAPP_ACCESS_TOKEN or "").strip().strip('"').strip("'")
        if raw_token.startswith("Bearer "):
            raw_token = raw_token[7:].strip()
        self.access_token = raw_token

        self.is_mock = not self.access_token or self.access_token == "dev_whatsapp_access_token"
        self.graph_version = "v20.0"
        self.base_url = f"https://graph.facebook.com/{self.graph_version}/{self.phone_number_id}"
        self.headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
        }

        # Log safe diagnostics without exposing secrets
        self.log_diagnostics()

    def get_diagnostics(self) -> dict[str, Any]:
        """Returns safe diagnostic metrics for authentication and endpoint configuration."""
        token_present = bool(self.access_token and self.access_token != "dev_whatsapp_access_token")
        token_len = len(self.access_token) if token_present else 0
        unexpected_prefix = bool(token_present and not self.access_token.startswith("EAA"))
        phone_id_present = bool(
            self.phone_number_id and self.phone_number_id != "dev_phone_number_id"
        )

        return {
            "token_present": token_present,
            "token_length": token_len,
            "unexpected_token_prefix": unexpected_prefix,
            "phone_number_id_present": phone_id_present,
            "graph_api_version": self.graph_version,
            "phone_number_id": self.phone_number_id,
            "is_mock": self.is_mock,
        }

    def log_diagnostics(self) -> None:
        """Logs safe diagnostic metrics without exposing access tokens or secrets."""
        diag = self.get_diagnostics()
        logger.info(
            "WhatsAppClient diagnostic configuration",
            token_present=diag["token_present"],
            token_length=diag["token_length"],
            unexpected_token_prefix=diag["unexpected_token_prefix"],
            phone_number_id_present=diag["phone_number_id_present"],
            graph_api_version=diag["graph_api_version"],
            phone_number_id=diag["phone_number_id"],
            is_mock=diag["is_mock"],
        )

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

            if resp.is_error:
                error_info: dict[str, Any] = {}
                try:
                    error_info = resp.json().get("error", {})
                except Exception:
                    error_info = {"raw_text": resp.text[:200]}

                logger.error(
                    "Meta WhatsApp API call failed",
                    status_code=resp.status_code,
                    error_message=error_info.get("message"),
                    error_type=error_info.get("type"),
                    error_code=error_info.get("code"),
                    error_subcode=error_info.get("error_subcode"),
                    fbtrace_id=error_info.get("fbtrace_id"),
                    phone_number_id=self.phone_number_id,
                    recipient=payload.get("to"),
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

        payload = {"messaging_product": "whatsapp", "status": "read", "message_id": to}
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.post(
                    f"{self.base_url}/messages",
                    json=payload,
                    headers=self.headers,
                    timeout=5.0,
                )
                if resp.is_error:
                    logger.warning(
                        "WhatsApp typing indicator status failed",
                        status_code=resp.status_code,
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
            return b"GIF89a\x01\x00\x01\x00\x80\x00\x00\xff\xff\xff\x00\x00\x00!\xf9\x04\x01\x00\x00\x00\x00,\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02D\x01\x00;"

        async with httpx.AsyncClient() as client:
            media_info_url = f"https://graph.facebook.com/{self.graph_version}/{media_id}"
            headers = {"Authorization": f"Bearer {self.access_token}"}

            resp = await client.get(media_info_url, headers=headers, timeout=15.0)
            if resp.is_error:
                error_info: dict[str, Any] = {}
                try:
                    error_info = resp.json().get("error", {})
                except Exception:
                    error_info = {"raw_text": resp.text[:200]}

                logger.error(
                    "Meta WhatsApp media info API call failed",
                    status_code=resp.status_code,
                    error_message=error_info.get("message"),
                    error_code=error_info.get("code"),
                    error_subcode=error_info.get("error_subcode"),
                    fbtrace_id=error_info.get("fbtrace_id"),
                    media_id=media_id,
                )
                resp.raise_for_status()

            download_url = resp.json().get("url")

            if not download_url:
                raise ValueError(
                    f"Download URL not found in metadata response for media_id: {media_id}"
                )

            media_binary_resp = await client.get(
                download_url, headers=headers, timeout=30.0
            )
            media_binary_resp.raise_for_status()
            return media_binary_resp.content
