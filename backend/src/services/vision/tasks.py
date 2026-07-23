import asyncio
from typing import Any
from uuid import UUID

import structlog
from celery.utils.log import get_task_logger

from src.db.session import AsyncSessionLocal
from src.repositories.ai import (
    FoodImageRepository,
    OCRResultRepository,
    VisionPredictionRepository,
)
from src.services.celery_app import celery_app
from src.services.vision.pipeline import VisionOCRPipeline

# Celery logger wrapper
logger = get_task_logger(__name__)
struct_logger = structlog.get_logger()


async def async_process_food_image(task_obj: Any, image_id: str) -> dict[str, Any]:
    """Asynchronously processes a food image: detects foods, estimates portions, and runs OCR scans.

    Args:
        task_obj: The Celery task instance (for retries).
        image_id: String UUID identifier of the FoodImage record.

    Returns:
        A dict containing execution results statistics.
    """
    image_uuid = UUID(image_id)

    async with AsyncSessionLocal() as db:
        image_repo = FoodImageRepository(db)
        ocr_repo = OCRResultRepository(db)
        pred_repo = VisionPredictionRepository(db)

        # 1. Fetch image
        image = await image_repo.get(image_uuid)
        if not image or image.deleted_at:
            struct_logger.error(
                "Food image record not found for background processing",
                image_id=image_id,
            )
            return {"status": "error", "message": "Food image not found"}

        # 2. Update status to processing
        image.status = "processing"
        db.add(image)
        await db.commit()

        try:
            pipeline = VisionOCRPipeline()

            # 3. Detect food items in background
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

            struct_logger.info(
                "Food image background processing complete",
                image_id=image_id,
                detected=predictions,
            )

            return {
                "status": "success",
                "image_id": image_id,
                "predictions_count": len(predictions),
                "predictions": predictions,
            }

        except Exception as e:
            await db.rollback()
            struct_logger.error(
                "Error processing food image task, retrying...",
                image_id=image_id,
                error=str(e),
            )
            # Trigger Celery retry mechanism
            try:
                raise task_obj.retry(exc=e)
            except Exception as retry_exc:
                # If retry count is exhausted, mark task as failed
                image.status = "failed"
                db.add(image)
                await db.commit()
                raise retry_exc


# Run task loop using asyncio event loop wrapper


@celery_app.task(
    name="src.services.vision.tasks.process_food_image_task",
    bind=True,
    max_retries=3,
    default_retry_delay=10,
)  # type: ignore[untyped-decorator]
def process_food_image_task(self: Any, image_id: str) -> dict[str, Any]:
    """Background task wrapper running the async food image processing loop."""
    return asyncio.run(async_process_food_image(self, image_id))
