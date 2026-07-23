import time
from uuid import UUID

import structlog
from sqlalchemy.ext.asyncio import AsyncSession

from src.services.ai.fallback_provider import FallbackProvider
from src.services.ai.gemini_provider import CircuitBreakerOpenError, GeminiProvider
from src.services.ai.interfaces import LLMProvider
from src.services.ai.memory import ConversationMemory
from src.services.ai.prompt_engine import PromptRenderer, SafetyValidator
from src.services.ai_service import (
    AIAnalyticsService,
    AIConversationService,
    AIPromptService,
)

logger = structlog.get_logger()


class AIOrchestrator:
    """Core AI Orchestrator coordinating prompt compilation, safety verification, LLM execution, failovers, and analytics logging."""

    def __init__(
        self,
        db: AsyncSession,
        primary_provider: LLMProvider | None = None,
        secondary_provider: LLMProvider | None = None,
    ) -> None:
        self.db = db
        self.primary = primary_provider or GeminiProvider()
        self.fallback = secondary_provider or FallbackProvider()
        self.prompt_service = AIPromptService(db)
        self.conv_service = AIConversationService(db)
        self.analytics_service = AIAnalyticsService(db)
        self.renderer = PromptRenderer()
        self.memory = ConversationMemory(db)

    async def process_chat_message(
        self,
        user_id: UUID,
        conversation_id: UUID,
        user_message: str,
    ) -> str:
        """Processes conversational messages running safety audits, contextual compilations, and logging details.

        Args:
            user_id: String UUID of the user.
            conversation_id: String UUID of the active conversation.
            user_message: Plaintext query from user.

        Returns:
            The conversational response string.
        """
        # 1. Audit input safety rules
        SafetyValidator.validate_input(user_message)

        # 2. Append user message to database history
        await self.conv_service.add_message(
            conversation_id=conversation_id,
            role="user",
            content=user_message,
            tokens=int(len(user_message) / 4),
        )
        await self.db.commit()

        # 3. Retrieve conversation history list context (manages window summarizations)
        history = await self.memory.get_chat_context(
            conversation_id=conversation_id,
            provider=self.primary,
        )

        # 4. Fetch the active prompt template configuration
        active_version = await self.prompt_service.get_active_prompt("coaching_agent")

        system_prompt = "You are a professional nutrition and fitness coach. Help the user log meals and track health targets."
        model_name = "gemini-1.5-flash"
        prompt_version_id = None

        if active_version:
            system_prompt = self.renderer.render_system_prompt(
                base_system_instructions=active_version.system_prompt
            )
            model_name = active_version.model_name
            prompt_version_id = active_version.id

        # 5. Run LLM execution wrapping primary and fallback channels
        start_time = time.time()
        response_text = ""
        used_fallback = False

        try:
            response_text = await self.primary.generate_response(
                system_prompt=system_prompt,
                prompt=user_message,
                history=history,
            )
        except (CircuitBreakerOpenError, Exception) as e:
            logger.error(
                "Primary GeminiProvider failed. Running fallback channel failover.",
                error=str(e),
                conversation_id=str(conversation_id),
            )
            used_fallback = True
            response_text = await self.fallback.generate_response(
                system_prompt=system_prompt,
                prompt=user_message,
                history=history,
            )

        duration_ms = int((time.time() - start_time) * 1000)

        # 6. Log response messages to database
        await self.conv_service.add_message(
            conversation_id=conversation_id,
            role="assistant",
            content=response_text,
            tokens=int(len(response_text) / 4),
        )
        await self.db.commit()

        # 7. Record usage analytics
        prompt_toks = int(len(user_message) / 4)
        completion_toks = int(len(response_text) / 4)
        cost = 0.0001 if not used_fallback else 0.0

        try:
            await self.analytics_service.log_request_response(
                user_id=user_id,
                prompt_version_id=prompt_version_id,
                request_payload={"message": user_message},
                response_payload={"reply": response_text},
                latency_ms=duration_ms,
                model_name=model_name if not used_fallback else "fallback-model",
                prompt_tokens=prompt_toks,
                completion_tokens=completion_toks,
                cost=cost,
            )
            await self.db.commit()
        except Exception as analytic_error:
            logger.warning(
                "Failed to log execution metrics to analytics dashboard database",
                error=str(analytic_error),
            )

        return response_text
