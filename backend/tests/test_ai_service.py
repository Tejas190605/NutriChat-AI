from uuid import uuid4

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from src.services.ai_service import (
    AIAnalyticsService,
    AIConversationService,
    AIPromptService,
    RecommendationService,
    VisionPersistenceService,
)


@pytest.mark.asyncio
async def test_conversations_prompts_and_recommendations_services(
    db_session: AsyncSession,
) -> None:
    """Verifies that all core services of the AI persistence data layer behave as expected."""
    if db_session is None:
        pytest.skip("Database is offline")

    user_id = uuid4()
    conv_service = AIConversationService(db_session)
    prompt_service = AIPromptService(db_session)
    rec_service = RecommendationService(db_session)
    vision_service = VisionPersistenceService(db_session)
    analytics_service = AIAnalyticsService(db_session)

    # 1. Test AIConversationService
    conv = await conv_service.start_conversation(user_id=user_id, title="Test Topic")
    assert conv.title == "Test Topic"
    assert conv.is_active is True

    msg = await conv_service.add_message(
        conversation_id=conv.id,
        role="user",
        content="Hello Coach!",
        tokens=10,
    )
    assert msg.role == "user"
    assert msg.content == "Hello Coach!"
    assert msg.tokens == 10

    # 2. Test AIPromptService
    template = await prompt_service.create_template(
        name="meal_parsing", description="Parses meal logs"
    )
    assert template.name == "meal_parsing"

    version = await prompt_service.create_version(
        template_id=template.id,
        version=1,
        system_prompt="You are a helper.",
        user_prompt_template="Log {food}",
        model_name="gemini-1.5-flash",
        temperature=0.5,
        is_active=True,
    )
    assert version.is_active is True
    assert version.model_name == "gemini-1.5-flash"

    active_v = await prompt_service.get_active_prompt("meal_parsing")
    assert active_v is not None
    assert active_v.version == 1

    # 3. Test RecommendationService
    rec = await rec_service.create_recommendation(
        user_id=user_id,
        category="alternative",
        content={"swap": "brown rice instead of white rice"},
    )
    assert rec.category == "alternative"

    feedback = await rec_service.add_feedback(
        rec_id=rec.id,
        user_id=user_id,
        feedback_value="liked",
        comments="Great swap suggestion!",
    )
    assert feedback.feedback_value == "liked"

    # 4. Test VisionPersistenceService
    img = await vision_service.log_food_image(
        user_id=user_id, image_url="http://example.com/food.jpg"
    )
    assert img.status == "uploaded"

    ocr = await vision_service.log_ocr_result(
        food_image_id=img.id, raw_text="Protein: 10g", parsed_json={"protein": 10}
    )
    assert ocr.raw_text == "Protein: 10g"

    pred = await vision_service.log_prediction(
        food_image_id=img.id, label="Apple", confidence=0.95
    )
    assert pred.label == "Apple"

    # 5. Test AIAnalyticsService
    req, resp = await analytics_service.log_request_response(
        user_id=user_id,
        prompt_version_id=version.id,
        request_payload={"food": "apple"},
        response_payload={"calories": 52},
        latency_ms=150,
        model_name="gemini-1.5-flash",
        prompt_tokens=5,
        completion_tokens=5,
        cost=0.0001,
    )
    assert req.user_id == user_id
    assert resp.latency_ms == 150
