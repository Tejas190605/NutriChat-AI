from typing import Any
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.v1.deps import get_current_user
from src.db.session import get_async_session
from src.models.user import User
from src.schemas.ai import AIConversationResponse, AIMessageResponse
from src.services.ai.meal_analyzer import MealAnalyzer
from src.services.ai.orchestrator import AIOrchestrator
from src.services.ai.recommendation_engine import RecommendationEngine
from src.services.ai_service import AIConversationService

router = APIRouter()


class ChatRequest(BaseModel):
    conversation_id: UUID
    message: str = Field(..., min_length=1, max_length=2000)


class MealAnalysisRequest(BaseModel):
    image_id: UUID


@router.post(
    "/chat",
    status_code=status.HTTP_200_OK,
    summary="Process conversational message utilizing AI Orchestration engine",
)
async def process_chat(
    payload: ChatRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_session),
) -> Any:
    """Sanitizes queries, renders prompt rules, runs Gemini/Fallback channels, and returns coaching replies.

    Args:
        payload: ChatRequest object containing message details.
        current_user: Currently authenticated user.
        db: SQLAlchemy async session instance.

    Returns:
        A dict response containing the coach text reply.
    """
    orchestrator = AIOrchestrator(db)
    try:
        reply = await orchestrator.process_chat_message(
            user_id=current_user.id,
            conversation_id=payload.conversation_id,
            user_message=payload.message,
        )
        return {"reply": reply}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        ) from e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"AI Orchestrator process failure: {str(e)}",
        ) from e


@router.post(
    "/analyze-meal",
    status_code=status.HTTP_200_OK,
    summary="Extract macronutrients totals from visual food detections and OCR results",
)
async def analyze_meal(
    payload: MealAnalysisRequest,
    _current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_session),
) -> Any:
    """Retrieves image logs, runs vision coordinate pipelines, aggregates calories, and calculates macro budgets.

    Args:
        payload: MealAnalysisRequest containing the image UUID.
        db: SQLAlchemy async session instance.

    Returns:
        A dictionary containing food detections and macro calculations.
    """
    analyzer = MealAnalyzer(db)
    try:
        return await analyzer.analyze_meal_image(payload.image_id)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        ) from e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Meal analysis processing error: {str(e)}",
        ) from e


@router.post(
    "/recommend",
    status_code=status.HTTP_200_OK,
    summary="Generate weight targets adjustments and Indian food swaps",
)
async def generate_recommendations(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_session),
) -> Any:
    """Computes daily deficits and returns target macronutrient splits.

    Args:
        current_user: Currently authenticated user.
        db: SQLAlchemy async session.

    Returns:
        A dictionary containing macro splits and recommendations.
    """
    engine = RecommendationEngine(db)
    try:
        return await engine.generate_macro_recommendations(current_user.id)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        ) from e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Recommendation engine execution failure: {str(e)}",
        ) from e


@router.get(
    "/conversations",
    response_model=list[AIConversationResponse],
    status_code=status.HTTP_200_OK,
    summary="List active conversation session histories metadata",
)
async def list_conversations(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_session),
) -> Any:
    """Returns active chat logs metadata."""
    service = AIConversationService(db)
    return await service.get_user_conversations(current_user.id)


@router.get(
    "/history",
    response_model=list[AIMessageResponse],
    status_code=status.HTTP_200_OK,
    summary="Fetch full messages logs list within a thread",
)
async def get_history(
    conversation_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_session),
) -> Any:
    """Retrieves all active messages stored inside the requested thread context.

    Args:
        conversation_id: UUID of the conversation thread.
        current_user: Currently authenticated user.
        db: Async database session.

    Returns:
        A list of AIMessageResponse objects.
    """
    service = AIConversationService(db)
    conv = await service.get_conversation(
        conversation_id=conversation_id, user_id=current_user.id
    )
    if not conv:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation context not found or unauthorized",
        )
    return [
        AIMessageResponse.model_validate(m) for m in conv.messages if not m.deleted_at
    ]
