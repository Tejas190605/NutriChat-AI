import hashlib
import json
from typing import Any, cast
from uuid import UUID, uuid4

import structlog
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.food_image import FoodImage
from src.repositories.ai import FoodImageRepository
from src.services.redis_client import get_redis_client
from src.services.vision.cloudinary_provider import CloudinaryStorageProvider
from src.services.vision.interfaces import OCRProvider, StorageProvider, VisionProvider
from src.services.vision.mock_providers import MockOCRProvider, MockVisionProvider
from src.services.vision.preprocessing import preprocess_image

logger = structlog.get_logger()


class ImageUploadPipeline:
    """Pipeline managing validations, preprocessing, uploads, and database logging of user images."""

    def __init__(
        self, db: AsyncSession, storage_provider: StorageProvider | None = None
    ) -> None:
        self.db = db
        self.storage = storage_provider or CloudinaryStorageProvider()
        self.image_repo = FoodImageRepository(db)

    async def upload_and_log(
        self, user_id: UUID, file_bytes: bytes, _original_filename: str
    ) -> FoodImage:
        """Validates format, compresses, resizes, uploads, and logs raw image references.

        Args:
            user_id: ID of the user uploading the image.
            file_bytes: Raw bytes of the image file.
            original_filename: Name of the original uploaded file.

        Returns:
            The created FoodImage SQLAlchemy model instance.
        """
        # 1. Image Preprocessing (resizing and compression)
        processed_bytes = preprocess_image(file_bytes)

        # 2. Upload to storage
        image_uuid = uuid4()
        clean_ext = ".jpg"
        storage_filename = f"{image_uuid}{clean_ext}"

        image_url = await self.storage.upload_image(processed_bytes, storage_filename)

        # 3. Create database entry
        food_image = await self.image_repo.create(
            {
                "id": image_uuid,
                "user_id": user_id,
                "image_url": image_url,
                "status": "uploaded",
            }
        )
        return food_image


class VisionOCRPipeline:
    """Orchestrates caching-enabled calls to Vision and OCR provider abstractions."""

    def __init__(
        self,
        vision_provider: VisionProvider | None = None,
        ocr_provider: OCRProvider | None = None,
        cache_ttl: int = 86400,
    ) -> None:
        self.vision = vision_provider or MockVisionProvider()
        self.ocr = ocr_provider or MockOCRProvider()
        self.cache_ttl = cache_ttl

    def _get_cache_key(self, prefix: str, target: str) -> str:
        """Generates a unique deterministic Redis key string for a query input."""
        sha = hashlib.sha256(target.encode("utf-8")).hexdigest()
        return f"vision:{prefix}:{sha}"

    async def detect_food(self, image_url: str) -> list[dict[str, Any]]:
        """Identifies food objects detected within the image, using Redis for caching."""
        cache_key = self._get_cache_key("detect", image_url)
        redis_client = get_redis_client()

        try:
            cached_val = await redis_client.get(cache_key)
            if cached_val:
                logger.info("Vision cache hit for food detection", url=image_url)
                return cast(list[dict[str, Any]], json.loads(cached_val))
        except Exception as e:
            logger.warning("Redis cache read error during food detection", error=str(e))

        # Perform the actual detection
        results = await self.vision.detect_food(image_url)

        try:
            await redis_client.setex(cache_key, self.cache_ttl, json.dumps(results))
        except Exception as e:
            logger.warning(
                "Redis cache write error during food detection", error=str(e)
            )

        return results

    async def estimate_portion(self, image_url: str, food_item: str) -> dict[str, Any]:
        """Estimates portion sizes, serving quantities, and weights with caching."""
        cache_key = self._get_cache_key("portion", f"{image_url}:{food_item}")
        redis_client = get_redis_client()

        try:
            cached_val = await redis_client.get(cache_key)
            if cached_val:
                logger.info(
                    "Vision cache hit for portion estimation", food_item=food_item
                )
                return cast(dict[str, Any], json.loads(cached_val))
        except Exception as e:
            logger.warning(
                "Redis cache read error during portion estimation", error=str(e)
            )

        results = await self.vision.estimate_portion(image_url, food_item)

        try:
            await redis_client.setex(cache_key, self.cache_ttl, json.dumps(results))
        except Exception as e:
            logger.warning(
                "Redis cache write error during portion estimation", error=str(e)
            )

        return results

    async def read_text(self, image_url: str) -> str:
        """Extracts raw text strings from labels with caching."""
        cache_key = self._get_cache_key("ocr_text", image_url)
        redis_client = get_redis_client()

        try:
            cached_val = await redis_client.get(cache_key)
            if cached_val:
                logger.info("OCR cache hit for raw text parsing", url=image_url)
                return str(cached_val)
        except Exception as e:
            logger.warning(
                "Redis cache read error during OCR text parsing", error=str(e)
            )

        text = await self.ocr.read_text(image_url)

        try:
            await redis_client.setex(cache_key, self.cache_ttl, text)
        except Exception as e:
            logger.warning(
                "Redis cache write error during OCR text parsing", error=str(e)
            )

        return text

    async def parse_nutrition_label(self, image_url: str) -> dict[str, Any]:
        """Parses nutritional value facts with caching."""
        cache_key = self._get_cache_key("nutrition_label", image_url)
        redis_client = get_redis_client()

        try:
            cached_val = await redis_client.get(cache_key)
            if cached_val:
                logger.info("OCR cache hit for nutrition label parsing", url=image_url)
                return cast(dict[str, Any], json.loads(cached_val))
        except Exception as e:
            logger.warning(
                "Redis cache read error during nutrition label parsing", error=str(e)
            )

        results = await self.ocr.parse_nutrition_label(image_url)

        try:
            await redis_client.setex(cache_key, self.cache_ttl, json.dumps(results))
        except Exception as e:
            logger.warning(
                "Redis cache write error during nutrition label parsing", error=str(e)
            )

        return results

    async def scan_barcode(self, image_url: str) -> str | None:
        """Extracts and decodes numeric barcode identifiers with caching."""
        cache_key = self._get_cache_key("barcode", image_url)
        redis_client = get_redis_client()

        try:
            cached_val = await redis_client.get(cache_key)
            if cached_val:
                logger.info("OCR cache hit for barcode scanning", url=image_url)
                return str(cached_val) if cached_val != "None" else None
        except Exception as e:
            logger.warning(
                "Redis cache read error during barcode scanning", error=str(e)
            )

        barcode = await self.ocr.scan_barcode(image_url)

        try:
            await redis_client.setex(
                cache_key,
                self.cache_ttl,
                str(barcode) if barcode is not None else "None",
            )
        except Exception as e:
            logger.warning(
                "Redis cache write error during barcode scanning", error=str(e)
            )

        return barcode
