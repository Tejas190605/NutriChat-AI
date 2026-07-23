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


class MealAnalyzer:
    """Analyzes uploads and combines predictions and OCR results into structured macronutrient details."""

    def __init__(
        self, db: AsyncSession, pipeline: VisionOCRPipeline | None = None
    ) -> None:
        self.db = db
        self.pipeline = pipeline or VisionOCRPipeline()
        self.image_repo = FoodImageRepository(db)
        self.ocr_repo = OCRResultRepository(db)
        self.pred_repo = VisionPredictionRepository(db)

    async def analyze_meal_image(self, image_id: UUID) -> dict[str, Any]:
        """Runs computer vision pipelines and aggregates macronutrients and calories calculations.

        Args:
            image_id: String UUID identifier of the FoodImage.

        Returns:
            A dictionary containing aggregated food items, macros, and confidence scores.
        """
        image = await self.image_repo.get(image_id)
        if not image or image.deleted_at:
            raise ValueError(f"Food image not found: {image_id}")

        logger.info(
            "Analyzing meal image details", image_id=str(image_id), url=image.image_url
        )

        # 1. Fetch Detections
        detected_foods = await self.pipeline.detect_food(image.image_url)

        # 2. Estimate Portions & collect predictions details
        aggregated_foods = []
        total_calories = 0
        total_protein = 0.0
        total_carbs = 0.0
        total_fat = 0.0
        confidence_sum = 0.0

        for item in detected_foods:
            label = item["label"]
            confidence = item["confidence"]
            confidence_sum += confidence

            portion = await self.pipeline.estimate_portion(image.image_url, label)

            # Estimate default macros based on food label names (mock reasoning rules)
            weight = portion.get("weight_grams", 100.0)
            factor = weight / 100.0

            # Dynamic mock macronutrients calculations matching standard ingredients
            if "apple" in label.lower():
                cals = int(52 * factor)
                prot = 0.3 * factor
                carbs = 14.0 * factor
                fat = 0.2 * factor
            elif "salad" in label.lower():
                cals = int(40 * factor)
                prot = 2.0 * factor
                carbs = 8.0 * factor
                fat = 0.5 * factor
            else:  # general Indian food defaults (e.g. paneer roti)
                cals = int(180 * factor)
                prot = 8.0 * factor
                carbs = 25.0 * factor
                fat = 6.0 * factor

            total_calories += cals
            total_protein += prot
            total_carbs += carbs
            total_fat += fat

            aggregated_foods.append(
                {
                    "label": label,
                    "confidence": confidence,
                    "portion": f"{portion.get('quantity', 1.0)} {portion.get('unit', 'serving')}",
                    "weight_grams": weight,
                    "calories": cals,
                }
            )

        # 3. Check OCR nutritional panel facts fallback
        parsed_label_macros = await self.pipeline.parse_nutrition_label(image.image_url)
        if parsed_label_macros and len(detected_foods) == 0:
            # Fallback to OCR parsed values directly if no foods were detected visually
            total_calories = parsed_label_macros.get("calories", 0)
            total_protein = parsed_label_macros.get("protein", 0.0)
            total_carbs = parsed_label_macros.get("carbs", 0.0)
            total_fat = parsed_label_macros.get("fat", 0.0)
            confidence_sum = 0.95
            aggregated_foods.append(
                {
                    "label": "Packaged Product Label",
                    "confidence": 0.95,
                    "portion": "1 pack",
                    "weight_grams": 100.0,
                    "calories": total_calories,
                }
            )

        avg_confidence = (
            confidence_sum / len(detected_foods) if detected_foods else 0.95
        )

        analysis_result = {
            "foods": aggregated_foods,
            "total_calories": total_calories,
            "total_protein": round(total_protein, 1),
            "total_carbs": round(total_carbs, 1),
            "total_fat": round(total_fat, 1),
            "confidence_score": round(avg_confidence, 2),
        }

        logger.info(
            "Meal analysis compiled", image_id=str(image_id), result=analysis_result
        )
        return analysis_result
