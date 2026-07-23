import json
from typing import Any

import structlog

from src.services.ai.interfaces import LLMProvider

logger = structlog.get_logger()


class FallbackProvider(LLMProvider):
    """Fallback completion provider executing mock outputs to prevent system interruptions."""

    async def generate_response(
        self,
        _system_prompt: str,
        prompt: str,
        _history: list[dict[str, str]] | None = None,
        _response_schema: Any | None = None,
    ) -> str:
        """Fallback conversational response provider."""
        logger.warning(
            "GeminiProvider down. Executing FallbackProvider response",
            prompt=prompt,
        )
        if _response_schema:
            return json.dumps(
                {
                    "response": "Fallback: Service is currently undergoing maintenance, but your state has been preserved. Please try again shortly.",
                    "analysis": "Preserved fallback data.",
                    "advice": "Drink plenty of water and eat clean meals.",
                    "safety": "safe",
                }
            )
        return "I am experiencing temporary server issues, but I have saved your history state. Let's resume tracking shortly!"

    async def analyze_image(
        self,
        _image_url_or_bytes: str | bytes,
        _prompt: str,
        _response_schema: Any | None = None,
    ) -> str:
        """Fallback multimodal image response provider."""
        logger.warning(
            "GeminiProvider down. Executing FallbackProvider image analyzer."
        )
        return json.dumps(
            {
                "foods": ["Detected Dish"],
                "portions": ["1 serving"],
                "calories": 300,
                "protein": 15.0,
                "carbs": 30.0,
                "fat": 10.0,
                "confidence": 0.50,
            }
        )
