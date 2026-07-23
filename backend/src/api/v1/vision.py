from typing import Any

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.v1.deps import get_current_user
from src.db.session import get_async_session
from src.models.user import User
from src.services.vision.pipeline import ImageUploadPipeline
from src.services.vision.tasks import process_food_image_task

router = APIRouter()


@router.post(
    "/upload",
    status_code=status.HTTP_201_CREATED,
    summary="Upload a food photo image and start background analytics processing",
)
async def upload_food_image(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_session),
) -> Any:
    """Accepts multipart image files, validates formats, resizes, uploads, and dispatches background tasks.

    Args:
        file: The uploaded image file.
        current_user: Currently authenticated user.
        db: SQLAlchemy async session instance.

    Returns:
        A dict containing status details and task info.
    """
    if not file.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Filename is missing or empty",
        )

    try:
        content = await file.read()
        pipeline = ImageUploadPipeline(db)

        # 1. Run pipeline (preprocessing, upload, database log creation)
        food_image = await pipeline.upload_and_log(
            user_id=current_user.id,
            file_bytes=content,
            _original_filename=file.filename,
        )

        # 2. Dispatch background Celery task
        process_food_image_task.delay(str(food_image.id))

        return {
            "status": "success",
            "message": "Image uploaded successfully. Background processing started.",
            "image_id": str(food_image.id),
            "image_url": food_image.image_url,
            "image_status": food_image.status,
        }

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        ) from e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Image upload pipeline execution error: {str(e)}",
        ) from e
