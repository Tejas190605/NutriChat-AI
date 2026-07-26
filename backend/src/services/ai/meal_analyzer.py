from typing import Any
from uuid import UUID

import structlog
from sqlalchemy.ext.asyncio import AsyncSession

from src.repositories.ai import (
    FoodImageRepository,
    OCRResultRepository,
    VisionPredictionRepository,
)
from src.services.nutrition.gemini_nutrition import GeminiNutritionEngine
from src.services.vision.pipeline import VisionOCRPipeline

logger = structlog.get_logger()


class MealAnalyzer:
    """Analyzes uploads and combines predictions and OCR results into structured macronutrient details using Gemini AI."""

    def __init__(
        self,
        db: AsyncSession,
        pipeline: VisionOCRPipeline | None = None,
        nutrition_engine: GeminiNutritionEngine | None = None,
    ) -> None:
        self.db = db
        self.pipeline = pipeline or VisionOCRPipeline()
        self.nutrition_engine = nutrition_engine or GeminiNutritionEngine()
        self.image_repo = FoodImageRepository(db)
        self.ocr_repo = OCRResultRepository(db)
        self.pred_repo = VisionPredictionRepository(db)

    async def analyze_meal_image(self, image_id: UUID) -> dict[str, Any]:
        """Runs computer vision pipelines and aggregates macronutrients and calories calculations via Gemini AI.

        Args:
            image_id: String UUID identifier of the FoodImage.

        Returns:
            A dictionary containing aggregated food items, macros, and confidence scores.
        """
        image = await self.image_repo.get(image_id)
        if not image or image.deleted_at:
            raise ValueError(f"Food image not found: {image_id}")

        logger.info(
            "Analyzing meal image details via Gemini AI",
            image_id=str(image_id),
            url=image.image_url,
        )

        # 1. Fetch Detections
        detected_foods = await self.pipeline.detect_food(image.image_url)

        # 2. Extract OCR raw nutrition data
        raw_ocr_text = await self.pipeline.read_text(image.image_url)
        parsed_ocr_json = await self.pipeline.parse_nutrition_label(image.image_url)

        vision_ocr_data = {
            "detected_foods": [f.get("label") for f in detected_foods],
            "raw_ocr_text": raw_ocr_text,
            "parsed_ocr": parsed_ocr_json,
        }

        # 3. Perform AI Nutrition estimation with Gemini Nutrition Engine
        food_query_name = ", ".join([f["label"] for f in detected_foods]) if detected_foods else "Uploaded Meal"
        nutrition_estimate = await self.nutrition_engine.estimate_nutrition(
            food_query=food_query_name,
            image_url_or_bytes=image.image_url,
            vision_ocr_data=vision_ocr_data,
        )

        # Build aggregated foods list
        aggregated_foods = []
        if detected_foods:
            for item in detected_foods:
                label = item["label"]
                confidence = item["confidence"]
                portion = await self.pipeline.estimate_portion(image.image_url, label)

                aggregated_foods.append(
                    {
                        "label": label,
                        "confidence": confidence,
                        "portion": f"{portion.get('quantity', 1.0)} {portion.get('unit', 'serving')}",
                        "weight_grams": portion.get("weight_grams", 150.0),
                        "calories": int(nutrition_estimate["estimated_calories"] / max(len(detected_foods), 1)),
                    }
                )
        else:
            aggregated_foods.append(
                {
                    "label": nutrition_estimate["food_name"],
                    "confidence": nutrition_estimate["confidence"],
                    "portion": nutrition_estimate["serving_size"],
                    "weight_grams": 200.0,
                    "calories": nutrition_estimate["estimated_calories"],
                }
            )

        analysis_result = {
            "foods": aggregated_foods,
            "total_calories": nutrition_estimate["estimated_calories"],
            "total_protein": nutrition_estimate["protein_g"],
            "total_carbs": nutrition_estimate["carbs_g"],
            "total_fat": nutrition_estimate["fat_g"],
            "fiber_g": nutrition_estimate["fiber_g"],
            "sugar_g": nutrition_estimate["sugar_g"],
            "sodium_mg": nutrition_estimate["sodium_mg"],
            "confidence_score": nutrition_estimate["confidence"],
            "reasoning": nutrition_estimate["reasoning"],
        }

        logger.info(
            "Meal analysis compiled with Gemini Nutrition Engine",
            image_id=str(image_id),
            result=analysis_result,
        )
        return analysis_result
