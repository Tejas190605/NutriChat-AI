from datetime import UTC, datetime
from uuid import UUID

import structlog
from sqlalchemy.ext.asyncio import AsyncSession

from src.repositories.ai import AIMessageRepository
from src.services.ai.interfaces import LLMProvider

logger = structlog.get_logger()


class ConversationMemory:
    """Manages short-term contexts, long-term database logs, and token window compression."""

    def __init__(
        self,
        db: AsyncSession,
        max_tokens: int = 1500,
        approximation_factor: float = 4.0,
    ) -> None:
        self.db = db
        self.max_tokens = max_tokens
        self.approximation_factor = approximation_factor
        self.msg_repo = AIMessageRepository(db)

    def _estimate_tokens(self, text: str) -> int:
        """Approximates the number of tokens based on character length."""
        return int(len(text) / self.approximation_factor)

    async def get_chat_context(
        self,
        conversation_id: UUID,
        provider: LLMProvider,
    ) -> list[dict[str, str]]:
        """Retrieves and prepares message context history, executing compression if limit exceeded."""
        # 1. Fetch active messages (order by created_at asc)
        messages = await self.msg_repo.get_conversation_messages(conversation_id)
        active_msgs = [m for m in messages if not m.deleted_at]

        # 2. Estimate tokens count
        total_estimated = 0
        for m in active_msgs:
            total_estimated += self._estimate_tokens(m.content)

        # 3. Trigger context compression if limit exceeded
        if total_estimated > self.max_tokens and len(active_msgs) > 6:
            logger.info(
                "Conversation token limit exceeded. Starting summarization compressions.",
                conversation_id=str(conversation_id),
                estimated_tokens=total_estimated,
                max_tokens=self.max_tokens,
            )
            # Summarize the first N-4 messages
            num_to_summarize = len(active_msgs) - 4
            to_summarize = active_msgs[:num_to_summarize]
            retaining = active_msgs[num_to_summarize:]

            # Compile text block to summarize
            summary_block = "\n".join(
                [f"{m.role.upper()}: {m.content}" for m in to_summarize]
            )

            system_summarize_prompt = "You are a helpful system agent. Summarize the following meal tracking conversation context into 3-4 bullet points highlighting user targets progress, preferences, and foods logged. Keep it highly concise."

            try:
                # Use provider to summarize
                summary_text = await provider.generate_response(
                    system_prompt=system_summarize_prompt,
                    prompt=summary_block,
                )

                # Soft delete the summarized messages
                for m in to_summarize:
                    m.deleted_at = datetime.now(UTC)
                    self.db.add(m)

                # Create a single summary system context block message
                summary_msg = await self.msg_repo.create(
                    {
                        "conversation_id": conversation_id,
                        "role": "system",
                        "content": f"[SYSTEM SUMMARY CONTEXT]: {summary_text}",
                        "tokens": self._estimate_tokens(summary_text),
                    }
                )

                await self.db.commit()

                # Reconstruct active messages context list
                compiled_context = [
                    {"role": summary_msg.role, "content": summary_msg.content}
                ]
                for m in retaining:
                    compiled_context.append({"role": m.role, "content": m.content})

                return compiled_context

            except Exception as e:
                logger.error(
                    "Failed to compress conversation context memory", error=str(e)
                )
                # Rollback and fallback to returning uncompressed
                await self.db.rollback()

        # Default mapping of history
        return [{"role": m.role, "content": m.content} for m in active_msgs]
