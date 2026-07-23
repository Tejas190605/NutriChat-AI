from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.models.ai_conversation import AIConversation
from src.models.ai_message import AIMessage
from src.models.food_image import FoodImage
from src.models.ocr_result import OCRResult
from src.models.prompt import PromptTemplate, PromptVersion
from src.models.recommendation import Recommendation, RecommendationFeedback
from src.models.usage import ModelUsage, TokenUsage
from src.models.vision_prediction import VisionPrediction
from src.repositories.base import BaseRepository


class AIConversationRepository(BaseRepository[AIConversation]):
    """Repository for AIConversation session management."""

    def __init__(self, db: AsyncSession):
        super().__init__(AIConversation, db)

    async def get_with_messages(self, conversation_id: UUID) -> AIConversation | None:
        """Retrieves a conversation preloading its messages history, ignoring soft deleted messages."""
        stmt = (
            select(self.model)
            .filter(self.model.id == conversation_id)
            .filter(self.model.deleted_at.is_(None))
            .options(selectinload(AIConversation.messages))
        )
        res = await self.db.execute(stmt)
        return res.scalars().first()

    async def get_user_conversations(self, user_id: UUID) -> list[AIConversation]:
        """Retrieves active conversations started by a user."""
        stmt = (
            select(self.model)
            .filter(self.model.user_id == user_id)
            .filter(self.model.deleted_at.is_(None))
            .order_by(self.model.created_at.desc())
        )
        res = await self.db.execute(stmt)
        return list(res.scalars().all())


class AIMessageRepository(BaseRepository[AIMessage]):
    """Repository for AIMessage operations."""

    def __init__(self, db: AsyncSession):
        super().__init__(AIMessage, db)


class PromptTemplateRepository(BaseRepository[PromptTemplate]):
    """Repository for PromptTemplate metadata operations."""

    def __init__(self, db: AsyncSession):
        super().__init__(PromptTemplate, db)

    async def get_by_name(self, name: str) -> PromptTemplate | None:
        """Finds a prompt template by name, preloading prompt versions."""
        stmt = (
            select(self.model)
            .filter(self.model.name == name)
            .filter(self.model.deleted_at.is_(None))
            .options(selectinload(PromptTemplate.versions))
        )
        res = await self.db.execute(stmt)
        return res.scalars().first()


class PromptVersionRepository(BaseRepository[PromptVersion]):
    """Repository for PromptVersion configurations operations."""

    def __init__(self, db: AsyncSession):
        super().__init__(PromptVersion, db)

    async def get_active_version(self, template_id: UUID) -> PromptVersion | None:
        """Retrieves the active prompt configuration version for a template."""
        stmt = (
            select(self.model)
            .filter(self.model.template_id == template_id)
            .filter(self.model.is_active.is_(True))
            .filter(self.model.deleted_at.is_(None))
        )
        res = await self.db.execute(stmt)
        return res.scalars().first()


class RecommendationRepository(BaseRepository[Recommendation]):
    """Repository for Recommendation operations."""

    def __init__(self, db: AsyncSession):
        super().__init__(Recommendation, db)

    async def get_user_recommendations(self, user_id: UUID) -> list[Recommendation]:
        """Retrieves suggestions logged for a user, preloading feed back ratings."""
        stmt = (
            select(self.model)
            .filter(self.model.user_id == user_id)
            .filter(self.model.deleted_at.is_(None))
            .options(selectinload(Recommendation.feedback))
        )
        res = await self.db.execute(stmt)
        return list(res.scalars().all())


class RecommendationFeedbackRepository(BaseRepository[RecommendationFeedback]):
    """Repository for RecommendationFeedback database interactions."""

    def __init__(self, db: AsyncSession):
        super().__init__(RecommendationFeedback, db)


class FoodImageRepository(BaseRepository[FoodImage]):
    """Repository for FoodImage files data."""

    def __init__(self, db: AsyncSession):
        super().__init__(FoodImage, db)


class OCRResultRepository(BaseRepository[OCRResult]):
    """Repository for OCRResult text results data."""

    def __init__(self, db: AsyncSession):
        super().__init__(OCRResult, db)


class VisionPredictionRepository(BaseRepository[VisionPrediction]):
    """Repository for VisionPrediction labels predictions."""

    def __init__(self, db: AsyncSession):
        super().__init__(VisionPrediction, db)


class TokenUsageRepository(BaseRepository[TokenUsage]):
    """Repository for TokenUsage statistics data."""

    def __init__(self, db: AsyncSession):
        super().__init__(TokenUsage, db)


class ModelUsageRepository(BaseRepository[ModelUsage]):
    """Repository for ModelUsage costs mapping calculations."""

    def __init__(self, db: AsyncSession):
        super().__init__(ModelUsage, db)

    async def get_by_model_name(self, model_name: str) -> ModelUsage | None:
        """Finds usage stats aggregating for a specific model key."""
        stmt = (
            select(self.model)
            .filter(self.model.model_name == model_name)
            .filter(self.model.deleted_at.is_(None))
        )
        res = await self.db.execute(stmt)
        return res.scalars().first()
