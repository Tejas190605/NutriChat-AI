import pytest
import json
from io import BytesIO
from uuid import uuid4
from PIL import Image
from sqlalchemy.ext.asyncio import AsyncSession
from src.services.vision.pipeline import ImageUploadPipeline, VisionOCRPipeline
from src.services.vision.mock_providers import MockVisionProvider, MockOCRProvider
from src.services.redis_client import get_redis_client
from src.services.vision.tasks import async_process_food_image


@pytest.mark.asyncio
async def test_image_upload_pipeline(db_session: AsyncSession) -> None:
    """Verifies that ImageUploadPipeline resizes, uploads, and logs records successfully."""
    if db_session is None:
        pytest.skip("Database is offline")

    user_id = uuid4()
    
    # 1. Create dummy image
    img = Image.new("RGB", (100, 100), color=(0, 255, 0))
    io_buf = BytesIO()
    img.save(io_buf, format="JPEG")
    raw_bytes = io_buf.getvalue()

    # 2. Run upload pipeline
    pipeline = ImageUploadPipeline(db_session)
    food_image = await pipeline.upload_and_log(
        user_id=user_id,
        file_bytes=raw_bytes,
        original_filename="apple.jpg",
    )

    # 3. Assertions
    assert food_image.user_id == user_id
    assert food_image.status == "uploaded"
    assert "static/uploads" in food_image.image_url


@pytest.mark.asyncio
async def test_vision_ocr_pipeline_caching() -> None:
    """Verifies that VisionOCRPipeline reads from and writes to Redis cache correctly."""
    redis_client = get_redis_client()
    try:
        # Ping Redis to verify connectivity
        await redis_client.ping()
    except Exception:
        pytest.skip("Redis is offline")

    image_url = f"http://example.com/test_salad_{uuid4()}.jpg"
    pipeline = VisionOCRPipeline()

    # 1. Trigger first call (should be a cache miss)
    detected_first = await pipeline.detect_food(image_url)
    assert len(detected_first) == 1
    assert detected_first[0]["label"] == "Green Salad"

    # 2. Modify value in mock provider to verify cache hit returns old value
    pipeline.vision = MockVisionProvider() # resets
    detected_second = await pipeline.detect_food(image_url)
    assert detected_second == detected_first

    # 3. Verify Redis has the cache key
    cache_key = pipeline._get_cache_key("detect", image_url)
    cached_val = await redis_client.get(cache_key)
    assert cached_val is not None
    assert "Green Salad" in str(cached_val)


@pytest.mark.asyncio
async def test_background_celery_task_processing(db_session: AsyncSession) -> None:
    """Verifies async background task queries and updates database records."""
    if db_session is None:
        pytest.skip("Database is offline")

    user_id = uuid4()
    
    # 1. Upload dummy food image first
    img = Image.new("RGB", (100, 100), color=(0, 255, 0))
    io_buf = BytesIO()
    img.save(io_buf, format="JPEG")
    raw_bytes = io_buf.getvalue()

    upload_pipeline = ImageUploadPipeline(db_session)
    food_image = await upload_pipeline.upload_and_log(
        user_id=user_id,
        file_bytes=raw_bytes,
        original_filename="salad.jpg",
    )
    
    # Ensure image_id is fully persisted
    await db_session.commit()

    # 2. Run background task logic synchronously
    result = await async_process_food_image(None, str(food_image.id))
    assert result["status"] == "success"
    assert result["predictions_count"] == 1
    assert result["predictions"][0] == "Green Salad"

    # Re-fetch image to check updated status
    async with db_session.begin_nested():
        await db_session.refresh(food_image)
        assert food_image.status == "completed"
