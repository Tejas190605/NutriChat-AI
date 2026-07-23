from typing import Any
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.v1.deps import get_current_user
from src.db.session import get_async_session
from src.models.user import User
from src.schemas.ai import (
    AIConversationCreate,
    AIConversationResponse,
    AIConversationUpdate,
    AIMessageCreate,
    AIMessageResponse,
    PromptTemplateCreate,
    PromptTemplateResponse,
    PromptVersionCreate,
    PromptVersionResponse,
    RecommendationCreate,
    RecommendationFeedbackCreate,
    RecommendationFeedbackResponse,
    RecommendationResponse,
)
from src.services.ai_service import (
    AIConversationService,
    AIPromptService,
    RecommendationService,
)

router = APIRouter()


# =====================================================================
# Conversation CRUD
# =====================================================================


@router.post(
    "/conversations",
    response_model=AIConversationResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Start a new AI conversation session",
)
async def start_conversation(
    payload: AIConversationCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_session),
) -> Any:
    """Initializes a new conversational thread tracker."""
    service = AIConversationService(db)
    return await service.start_conversation(
        user_id=current_user.id, title=payload.title
    )


@router.get(
    "/conversations",
    response_model=list[AIConversationResponse],
    status_code=status.HTTP_200_OK,
    summary="List active conversation sessions for the current user",
)
async def list_conversations(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_session),
) -> Any:
    """Retrieves all active conversation threads logged for the current user."""
    service = AIConversationService(db)
    return await service.get_user_conversations(user_id=current_user.id)


@router.get(
    "/conversations/{conversation_id}",
    response_model=dict[str, Any],
    status_code=status.HTTP_200_OK,
    summary="Retrieve conversation details with messages list history",
)
async def get_conversation(
    conversation_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_session),
) -> Any:
    """Fetches full messages history within a conversational thread context."""
    service = AIConversationService(db)
    conv = await service.get_conversation(
        conversation_id=conversation_id, user_id=current_user.id
    )
    if not conv:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found or unauthorized",
        )
    return {
        "id": conv.id,
        "user_id": conv.user_id,
        "title": conv.title,
        "is_active": conv.is_active,
        "created_at": conv.created_at,
        "updated_at": conv.updated_at,
        "messages": [
            AIMessageResponse.model_validate(m)
            for m in conv.messages
            if not m.deleted_at
        ],
    }


@router.post(
    "/conversations/{conversation_id}/messages",
    response_model=AIMessageResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Append a new message to the conversation",
)
async def add_message(
    conversation_id: UUID,
    payload: AIMessageCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_session),
) -> Any:
    """Logs a user/assistant reply to the thread history."""
    service = AIConversationService(db)
    # Check permissions first
    conv = await service.get_conversation(
        conversation_id=conversation_id, user_id=current_user.id
    )
    if not conv:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found or unauthorized",
        )
    try:
        return await service.add_message(
            conversation_id=conversation_id,
            role=payload.role,
            content=payload.content,
            tokens=payload.tokens,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        ) from e


@router.put(
    "/conversations/{conversation_id}",
    response_model=AIConversationResponse,
    status_code=status.HTTP_200_OK,
    summary="Update conversation title or toggle status",
)
async def update_conversation(
    conversation_id: UUID,
    payload: AIConversationUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_session),
) -> Any:
    """Updates title metadata or closes active chat session logs."""
    service = AIConversationService(db)
    conv = await service.get_conversation(
        conversation_id=conversation_id, user_id=current_user.id
    )
    if not conv:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found or unauthorized",
        )

    update_dict: dict[str, Any] = {}
    if payload.title is not None:
        update_dict["title"] = payload.title
    if payload.is_active is not None:
        update_dict["is_active"] = payload.is_active

    if update_dict:
        await service.conv_repo.update(conv, update_dict)

    return conv


@router.delete(
    "/conversations/{conversation_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Soft delete conversation session history logs",
)
async def delete_conversation(
    conversation_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_session),
) -> None:
    """Soft deletes chat logs records."""
    service = AIConversationService(db)
    success = await service.delete_conversation(
        conversation_id=conversation_id, user_id=current_user.id
    )
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found or unauthorized",
        )


# =====================================================================
# Prompt Template CRUD
# =====================================================================


@router.post(
    "/prompts/templates",
    response_model=PromptTemplateResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new prompt template metadata header",
)
async def create_template(
    payload: PromptTemplateCreate,
    _current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_session),
) -> Any:
    """Registers a prompt category identifier (Admin only guard is implicit since JWT is required)."""
    service = AIPromptService(db)
    return await service.create_template(
        name=payload.name, description=payload.description
    )


@router.post(
    "/prompts/templates/{template_id}/versions",
    response_model=PromptVersionResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new prompt version configuration template",
)
async def create_version(
    template_id: UUID,
    payload: PromptVersionCreate,
    _current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_session),
) -> Any:
    """Pushes a template formatting version, deactivating others if is_active=True."""
    service = AIPromptService(db)
    try:
        return await service.create_version(
            template_id=template_id,
            version=payload.version,
            system_prompt=payload.system_prompt,
            user_prompt_template=payload.user_prompt_template,
            model_name=payload.model_name,
            temperature=payload.temperature,
            is_active=payload.is_active,
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e


@router.get(
    "/prompts/templates/{name}/active",
    response_model=PromptVersionResponse,
    status_code=status.HTTP_200_OK,
    summary="Fetch the active version config for a template",
)
async def get_active_prompt(
    name: str,
    _current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_session),
) -> Any:
    """Returns active templates guidelines to parse incoming WhatsApp texts."""
    service = AIPromptService(db)
    version = await service.get_active_prompt(name=name)
    if not version:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Active version for prompt '{name}' not found",
        )
    return version


# =====================================================================
# Recommendation CRUD & Feedback CRUD
# =====================================================================


@router.post(
    "/recommendations",
    response_model=RecommendationResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new recommendation log",
)
async def create_recommendation(
    payload: RecommendationCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_session),
) -> Any:
    """Logs suggestions payload logs."""
    service = RecommendationService(db)
    return await service.create_recommendation(
        user_id=current_user.id,
        category=payload.category,
        content=payload.content,
    )


@router.post(
    "/recommendations/{recommendation_id}/feedback",
    response_model=RecommendationFeedbackResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Log rating feedback for a suggestion",
)
async def log_feedback(
    recommendation_id: UUID,
    payload: RecommendationFeedbackCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_session),
) -> Any:
    """Registers user ratings feedback logs."""
    service = RecommendationService(db)
    try:
        return await service.add_feedback(
            rec_id=recommendation_id,
            user_id=current_user.id,
            feedback_value=payload.feedback_value,
            comments=payload.comments,
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e
