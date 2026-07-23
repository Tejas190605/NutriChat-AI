from typing import Any

import structlog

logger = structlog.get_logger()


class SafetyValidator:
    """Validator inspecting chat inputs for jailbreak attempts or toxic constructs."""

    UNSAFE_KEYWORDS = [
        "ignore previous instructions",
        "system prompt",
        "bypass filters",
        "jailbreak",
        "self-harm",
        "suicide",
        "bomb",
        "exploding",
        "hate speech",
        "kill myself",
    ]

    @classmethod
    def validate_input(cls, user_text: str) -> bool:
        """Scans raw user text for policy or safety violations.

        Args:
            user_text: Raw string input message.

        Returns:
            True if text is compliant.

        Raises:
            ValueError: If unsafe content matches keywords patterns.
        """
        text_lower = user_text.lower()
        for keyword in cls.UNSAFE_KEYWORDS:
            if keyword in text_lower:
                logger.warning(
                    "Unsafe keyword match detected in chat text input",
                    matched_keyword=keyword,
                )
                raise ValueError("Input message violates safety policy constraints.")
        return True


class PromptRenderer:
    """Manager to render prompts, formatting variable templates, system personas, and outputs schemas."""

    def __init__(self) -> None:
        pass

    def render_system_prompt(
        self, base_system_instructions: str, response_schema: Any | None = None
    ) -> str:
        """Appends output format guidelines to the base system prompt.

        Args:
            base_system_instructions: Standard coach system persona prompt.
            response_schema: Optional output target schema.

        Returns:
            The compiled system instructions string.
        """
        prompt = base_system_instructions
        if response_schema:
            prompt += (
                "\n\nCRITICAL REQUIREMENT: You MUST reply with a valid JSON payload matching "
                "the fields of this schema exactly: "
                f"{response_schema.__doc__ or response_schema.__name__}. Do not wrap response in markdown blocks."
            )
        return prompt

    def render_user_prompt(self, template_str: str, variables: dict[str, Any]) -> str:
        """Interpolates variables inside prompt formatting templates.

        Args:
            template_str: Template string with format placeholders (e.g. "{food}").
            variables: Context variables dictionary to replace.

        Returns:
            The formatted user prompt string.
        """
        try:
            return template_str.format(**variables)
        except KeyError as e:
            logger.error(
                "Failed to render prompt template variables",
                error=str(e),
                template=template_str,
            )
            # Safe fallback: raw string replacement
            return template_str
