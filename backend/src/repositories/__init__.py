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
from src.repositories.barcode import BarcodeRepository
from src.repositories.base import BaseRepository
from src.repositories.meal import MealRepository
from src.repositories.nutrition import (
    FavoriteFoodRepository,
    FoodCategoryRepository,
    FoodRepository,
    RecentFoodRepository,
)
from src.repositories.token import RefreshTokenRepository
from src.repositories.user import UserRepository

__all__ = [
    "BaseRepository",
    "UserRepository",
    "RefreshTokenRepository",
    "FoodRepository",
    "FoodCategoryRepository",
    "FavoriteFoodRepository",
    "RecentFoodRepository",
    "MealRepository",
    "BarcodeRepository",
    "AIConversationRepository",
    "AIMessageRepository",
    "PromptTemplateRepository",
    "PromptVersionRepository",
    "RecommendationRepository",
    "RecommendationFeedbackRepository",
    "FoodImageRepository",
    "OCRResultRepository",
    "VisionPredictionRepository",
    "TokenUsageRepository",
    "ModelUsageRepository",
]
