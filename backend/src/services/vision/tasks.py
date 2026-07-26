from typing import Any
from uuid import UUID

import structlog
from sqlalchemy.ext.asyncio import AsyncSession

from src.repositories.ai import (
    FoodImageRepository,
    OCRResultRepository,
    VisionPredictionRepository,
)
from src.services.vision.pipeline import VisionOCRPipeline

logger = structlog.get_logger()


async def process_food_image(db: AsyncSession, image_id: UUID) -> dict[str, Any]:
    """Synchronously/Directly processes a food image within the FastAPI request cycle.

    Detects foods, estimates portions, and runs OCR scans without background worker queues.

    Args:
        db: Active SQLAlchemy AsyncSession.
        image_id: UUID identifier of the FoodImage record.

    Returns:
        A dict containing execution results statistics.
    """
    image_repo = FoodImageRepository(db)
    ocr_repo = OCRResultRepository(db)
    pred_repo = VisionPredictionRepository(db)

    # 1. Fetch image
    image = await image_repo.get(image_id)
    if not image or image.deleted_at:
        logger.error(
            "Food image record not found for processing",
            image_id=str(image_id),
        )
        return {"status": "error", "message": "Food image not found"}

    # 2. Update status to processing
    image.status = "processing"
    db.add(image)
    await db.commit()

    try:
        pipeline = VisionOCRPipeline()

        # 3. Detect food items
        detected_foods = await pipeline.detect_food(image.image_url)

        # 4. For each food item, run portion estimation and persist prediction
        predictions = []
        for item in detected_foods:
            label = item["label"]
            confidence = item["confidence"]
            coords = item.get("box_coordinates")

            # Portion estimation
            portion = await pipeline.estimate_portion(image.image_url, label)

            # Combine coordinate details and portion sizes
            payload = {
                "box_coordinates": coords,
                "portion_estimation": portion,
            }

            pred = await pred_repo.create(
                {
                    "food_image_id": image.id,
                    "label": label,
                    "confidence": confidence,
                    "box_coordinates": payload,
                }
            )
            predictions.append(pred.label)

        # 5. Extract OCR raw nutrition data
        raw_text = await pipeline.read_text(image.image_url)
        parsed_json = await pipeline.parse_nutrition_label(image.image_url)

        await ocr_repo.create(
            {
                "food_image_id": image.id,
                "raw_text": raw_text,
                "parsed_json": parsed_json,
            }
        )

        # 6. Mark image processing completed
        image.status = "completed"
        db.add(image)
        await db.commit()

        logger.info(
            "Food image processing complete",
            image_id=str(image_id),
            detected=predictions,
        )

        return {
            "status": "success",
            "image_id": str(image_id),
            "predictions_count": len(predictions),
            "predictions": predictions,
        }

    except Exception as e:
        await db.rollback()
        image.status = "failed"
        db.add(image)
        await db.commit()
        logger.error(
            "Error processing food image",
            image_id=str(image_id),
            error=str(e),
        )
        raise e


# Backward compatibility wrapper for existing tests
async def async_process_food_image(task_obj: Any, image_id: str) -> dict[str, Any]:
    """Compatibility wrapper for direct test invocations."""
    from src.db.session import AsyncSessionLocal

    async with AsyncSessionLocal() as session:
        return await process_food_image(session, UUID(image_id))
