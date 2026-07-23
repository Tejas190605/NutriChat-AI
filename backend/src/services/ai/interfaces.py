from abc import ABC, abstractmethod
from typing import Any


class LLMProvider(ABC):
    """Abstract interface contract for conversational completions and structured analysis."""

    @abstractmethod
    async def generate_response(
        self,
        system_prompt: str,
        prompt: str,
        history: list[dict[str, str]] | None = None,
        response_schema: Any | None = None,
    ) -> str:
        """Generates conversational completions based on context and prompts.

        Args:
            system_prompt: System guidelines/persona framing.
            prompt: Direct query or user message text.
            history: Optional list of chat history messages mapping {"role": "...", "content": "..."}.
            response_schema: Pydantic base model class if structured JSON output is requested.

        Returns:
            The raw text response from the provider.
        """
        pass

    @abstractmethod
    async def analyze_image(
        self,
        image_url_or_bytes: str | bytes,
        prompt: str,
        response_schema: Any | None = None,
    ) -> str:
        """Processes multimodal image payload queries with instructions.

        Args:
            image_url_or_bytes: Image URL string or raw bytes data.
            prompt: Guidelines for the model (e.g. food recognition prompt).
            response_schema: Optional Pydantic schema for structured output.

        Returns:
            A string response containing model outputs.
        """
        pass
