import uuid
from datetime import UTC, datetime
from typing import Any
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from src.models.ai_conversation import AIConversation
from src.models.ai_message import AIMessage
from src.models.ai_request_response import AIRequest, AIResponse
from src.models.food_image import FoodImage
from src.models.ocr_result import OCRResult
from src.models.prompt import PromptTemplate, PromptVersion
from src.models.recommendation import Recommendation, RecommendationFeedback
from src.models.usage import TokenUsage
from src.models.vision_prediction import VisionPrediction
from src.repositories.ai import (
    AIConversationRepository,
    AIMessageRepository,
    FoodImageRepository,
    ModelUsageRepository,
    OCRResultRepository,
    PromptTemplateRepository,
    PromptVersionRepository,
    RecommendationFeedbackRepository,
    RecommendationRepository,
    TokenUsageRepository,
    VisionPredictionRepository,
)


class AIConversationService:
    """Service for managing AI conversational session contexts and chat histories."""

    def __init__(self, db: AsyncSession):
        self.db = db
        self.conv_repo = AIConversationRepository(db)
        self.msg_repo = AIMessageRepository(db)

    async def start_conversation(
        self, user_id: UUID, title: str | None = None
    ) -> AIConversation:
        """Starts a new AI conversation session."""
        return await self.conv_repo.create(
            {
                "user_id": user_id,
                "title": title,
                "is_active": True,
            }
        )

    async def add_message(
        self, conversation_id: UUID, role: str, content: str, tokens: int | None = None
    ) -> AIMessage:
        """Appends a new role message to an active conversation context history."""
        # Verify conversation exists and is active
        conv = await self.conv_repo.get(conversation_id)
        if not conv or not conv.is_active or conv.deleted_at:
            raise ValueError("Conversation not found or is inactive")

        msg = await self.msg_repo.create(
            {
                "conversation_id": conversation_id,
                "role": role,
                "content": content,
                "tokens": tokens,
            }
        )
        conv.updated_at = datetime.now(UTC)
        self.db.add(conv)
        await self.db.flush()
        return msg

    async def get_conversation(
        self, conversation_id: UUID, user_id: UUID
    ) -> AIConversation | None:
        """Retrieves a conversation checking owner privileges."""
        conv = await self.conv_repo.get_with_messages(conversation_id)
        if not conv or conv.user_id != user_id or conv.deleted_at:
            return None
        return conv

    async def get_user_conversations(self, user_id: UUID) -> list[AIConversation]:
        """Retrieves all active conversations started by a user."""
        return await self.conv_repo.get_user_conversations(user_id)

    async def delete_conversation(self, conversation_id: UUID, user_id: UUID) -> bool:
        """Performs soft delete on conversation history files."""
        conv = await self.conv_repo.get(conversation_id)
        if not conv or conv.user_id != user_id or conv.deleted_at:
            return False
        conv.deleted_at = datetime.now(UTC)
        self.db.add(conv)
        await self.db.flush()
        return True


class AIPromptService:
    """Service managing PromptTemplate versions registries."""

    def __init__(self, db: AsyncSession):
        self.db = db
        self.template_repo = PromptTemplateRepository(db)
        self.version_repo = PromptVersionRepository(db)

    async def create_template(
        self, name: str, description: str | None = None
    ) -> PromptTemplate:
        """Creates a prompt template metadata header."""
        return await self.template_repo.create(
            {
                "name": name,
                "description": description,
            }
        )

    async def get_template(self, template_id: UUID) -> PromptTemplate | None:
        """Retrieves a prompt template metadata header."""
        template = await self.template_repo.get(template_id)
        if not template or template.deleted_at:
            return None
        return template

    async def create_version(
        self,
        template_id: UUID,
        version: int,
        system_prompt: str,
        user_prompt_template: str,
        model_name: str,
        temperature: float = 0.7,
        is_active: bool = False,
    ) -> PromptVersion:
        """Registers a new prompt version configuration template."""
        template = await self.template_repo.get(template_id)
        if not template or template.deleted_at:
            raise ValueError("Template not found")

        # If this version is marked active, deactivate others
        if is_active:
            from sqlalchemy import update

            await self.db.execute(
                update(PromptVersion)
                .where(PromptVersion.template_id == template_id)
                .values(is_active=False)
            )

        prompt_version = await self.version_repo.create(
            {
                "template_id": template_id,
                "version": version,
                "system_prompt": system_prompt,
                "user_prompt_template": user_prompt_template,
                "model_name": model_name,
                "temperature": temperature,
                "is_active": is_active,
            }
        )
        return prompt_version

    async def get_active_prompt(self, name: str) -> PromptVersion | None:
        """Fetches the currently active prompt version for a template named name."""
        template = await self.template_repo.get_by_name(name)
        if not template:
            return None
        return await self.version_repo.get_active_version(template.id)


class RecommendationService:
    """Service managing recommendation suggestions logs and ratings feedback logs."""

    def __init__(self, db: AsyncSession):
        self.db = db
        self.rec_repo = RecommendationRepository(db)
        self.feedback_repo = RecommendationFeedbackRepository(db)

    async def create_recommendation(
        self, user_id: UUID, category: str, content: dict[str, Any]
    ) -> Recommendation:
        """Logs recommendation suggestions generated for a user."""
        return await self.rec_repo.create(
            {
                "user_id": user_id,
                "category": category,
                "content": content,
            }
        )

    async def get_recommendation(
        self, rec_id: UUID, user_id: UUID
    ) -> Recommendation | None:
        """Retrieves logged recommendation checking user permissions."""
        rec = await self.rec_repo.get(rec_id)
        if not rec or rec.user_id != user_id or rec.deleted_at:
            return None
        return rec

    async def add_feedback(
        self,
        rec_id: UUID,
        user_id: UUID,
        feedback_value: str,
        comments: str | None = None,
    ) -> RecommendationFeedback:
        """Logs rating feedback for a suggestion."""
        rec = await self.rec_repo.get(rec_id)
        if not rec or rec.user_id != user_id or rec.deleted_at:
            raise ValueError("Recommendation not found or unauthorized")

        return await self.feedback_repo.create(
            {
                "recommendation_id": rec_id,
                "feedback_value": feedback_value,
                "comments": comments,
            }
        )


class VisionPersistenceService:
    """Service orchestrating raw uploads logging, OCR scan results, and CV prediction labels."""

    def __init__(self, db: AsyncSession):
        self.db = db
        self.image_repo = FoodImageRepository(db)
        self.ocr_repo = OCRResultRepository(db)
        self.pred_repo = VisionPredictionRepository(db)

    async def log_food_image(
        self, user_id: UUID, image_url: str, status: str = "uploaded"
    ) -> FoodImage:
        """Creates a record of user photo uploads."""
        return await self.image_repo.create(
            {
                "user_id": user_id,
                "image_url": image_url,
                "status": status,
            }
        )

    async def log_ocr_result(
        self,
        food_image_id: UUID,
        raw_text: str,
        parsed_json: dict[str, Any] | None = None,
    ) -> OCRResult:
        """Persists OCR parsed label data linked to a food image upload."""
        return await self.ocr_repo.create(
            {
                "food_image_id": food_image_id,
                "raw_text": raw_text,
                "parsed_json": parsed_json,
            }
        )

    async def log_prediction(
        self,
        food_image_id: UUID,
        label: str,
        confidence: float,
        box_coordinates: dict[str, Any] | None = None,
    ) -> VisionPrediction:
        """Logs bounding boxes coordinates and confidences score predictions."""
        return await self.pred_repo.create(
            {
                "food_image_id": food_image_id,
                "label": label,
                "confidence": confidence,
                "box_coordinates": box_coordinates,
            }
        )


class AIAnalyticsService:
    """Service tracking prompt execution logs, latencies, token consumption counts, and model costs."""

    def __init__(self, db: AsyncSession):
        self.db = db
        self.request_repo = TokenUsageRepository(db).db  # Generic fallback db session
        self.usage_repo = TokenUsageRepository(db)
        self.model_repo = ModelUsageRepository(db)

    async def log_request_response(
        self,
        user_id: UUID | None,
        prompt_version_id: UUID | None,
        request_payload: dict[str, Any],
        response_payload: dict[str, Any],
        latency_ms: int,
        model_name: str,
        prompt_tokens: int,
        completion_tokens: int,
        cost: float = 0.0,
    ) -> tuple[AIRequest, AIResponse]:
        """Atomically logs AI request payloads, response texts, and tokens used, updating model stats."""
        # 1. Create AIRequest
        req = AIRequest(
            id=uuid.uuid4(),
            user_id=user_id,
            prompt_version_id=prompt_version_id,
            request_payload=request_payload,
        )
        self.db.add(req)
        await self.db.flush()

        # 2. Create AIResponse
        resp = AIResponse(
            id=uuid.uuid4(),
            request_id=req.id,
            response_payload=response_payload,
            latency_ms=latency_ms,
        )
        self.db.add(resp)

        # 3. Create TokenUsage
        usage = TokenUsage(
            id=uuid.uuid4(),
            user_id=user_id,
            request_id=req.id,
            model_name=model_name,
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            total_tokens=prompt_tokens + completion_tokens,
            cost=cost,
        )
        self.db.add(usage)

        # 4. Increment ModelUsage aggregation cost
        model_usage = await self.model_repo.get_by_model_name(model_name)
        if model_usage:
            model_usage.call_count += 1
            model_usage.total_prompt_tokens += prompt_tokens
            model_usage.total_completion_tokens += completion_tokens
            model_usage.total_cost += cost
            self.db.add(model_usage)
        else:
            await self.model_repo.create(
                {
                    "model_name": model_name,
                    "call_count": 1,
                    "total_prompt_tokens": prompt_tokens,
                    "total_completion_tokens": completion_tokens,
                    "total_cost": cost,
                }
            )

        await self.db.flush()
        return req, resp
