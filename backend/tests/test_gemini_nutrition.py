import pytest

from src.services.nutrition.gemini_nutrition import GeminiNutritionEngine


@pytest.mark.asyncio
async def test_gemini_nutrition_engine_text_query() -> None:
    """Verifies that GeminiNutritionEngine processes text food queries correctly."""
    engine = GeminiNutritionEngine()

    result = await engine.estimate_nutrition(food_query="1 Apple")

    assert result["food_name"] == "1 Apple"
    assert "estimated_calories" in result
    assert "protein_g" in result
    assert "carbs_g" in result
    assert "fat_g" in result
    assert result["confidence"] >= 0.70
    assert "reasoning" in result


@pytest.mark.asyncio
async def test_gemini_nutrition_engine_vision_ocr_query() -> None:
    """Verifies that GeminiNutritionEngine estimates macros from vision and OCR data."""
    engine = GeminiNutritionEngine()

    vision_data = {
        "detected_foods": ["Green Salad", "Grilled Chicken"],
        "raw_ocr_text": "Calories 350 Protein 30g Carbs 10g Fat 8g",
    }

    result = await engine.estimate_nutrition(
        food_query="Salad Plate", vision_ocr_data=vision_data
    )

    assert "estimated_calories" in result
    assert result["estimated_calories"] > 0
    assert result["protein_g"] > 0
    assert result["carbs_g"] >= 0
    assert result["fat_g"] >= 0
