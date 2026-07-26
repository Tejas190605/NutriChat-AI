import json
from typing import Any

import structlog

logger = structlog.get_logger()

GEMINI_NUTRITION_SYSTEM_PROMPT = """You are an expert AI Nutritionist, Food Scientist, and Clinical Dietitian.
Your mission is to estimate comprehensive macronutrient and micronutrient values for meals, food items, packaged goods, and recipes.

Given a food name, description, image, or combined OCR/vision input, provide a realistic, conservative, evidence-based nutritional breakdown.

RULES:
1. Estimate total calories (kcal), protein (g), carbohydrates (g), fat (g), fiber (g), sugar (g), and sodium (mg).
2. Specify the estimated serving size (e.g., "1 plate (approx 250g)", "1 medium piece (150g)").
3. Assign a confidence score between 0.00 and 1.00 based on input clarity.
4. Provide concise scientific reasoning explaining how the portion and macro splits were derived.
5. Use conservative, realistic nutritional estimates. Never hallucinate impossible values (e.g. 100g of chicken breast cannot contain 200g of protein).
6. ALWAYS respond with valid JSON matching EXACTLY the following structure:

{
  "food_name": "Name or description of the food item",
  "estimated_calories": 250,
  "protein_g": 12.5,
  "carbs_g": 30.0,
  "fat_g": 8.0,
  "fiber_g": 4.5,
  "sugar_g": 5.0,
  "sodium_mg": 320.0,
  "serving_size": "1 serving (200g)",
  "confidence": 0.90,
  "reasoning": "Reasoning detailing macro calculation and portion assumptions."
}
"""


class GeminiNutritionEngine:
    """Zero-cost AI Nutrition Engine powered by Google Gemini AI.

    Replaces third-party paid nutrition lookup APIs with structured LLM estimations.
    """

    def __init__(self, provider: Any | None = None) -> None:
        if provider is None:
            from src.services.ai.gemini_provider import GeminiProvider

            self.provider = GeminiProvider()
        else:
            self.provider = provider

    async def estimate_nutrition(
        self,
        food_query: str | None = None,
        image_url_or_bytes: str | bytes | None = None,
        vision_ocr_data: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Estimates complete nutrition details using text, image, or vision/OCR data inputs.

        Args:
            food_query: Text food description or item name.
            image_url_or_bytes: Image URL string or raw bytes for multimodal estimation.
            vision_ocr_data: Pre-processed vision bounding box or OCR text dictionary.

        Returns:
            A structured dict containing food_name, calories, macros, confidence, and reasoning.
        """
        logger.info(
            "Executing Gemini Nutrition Engine estimation",
            query=food_query,
            has_image=bool(image_url_or_bytes),
            has_vision_data=bool(vision_ocr_data),
        )

        # 1. Fallback / Mock mode when Gemini API key is default or provider in mock state
        if getattr(self.provider, "is_mock", True):
            return self._build_mock_nutrition(food_query, vision_ocr_data)

        try:
            # 2. Multimodal estimation if image is provided directly
            if image_url_or_bytes:
                prompt = (
                    f"Analyze this food image and estimate its nutrition facts. "
                    f"Context / query: '{food_query or 'Identify meal'}'."
                )
                if vision_ocr_data:
                    prompt += f" OCR / Vision hints: {json.dumps(vision_ocr_data)}"

                raw_json = await self.provider.analyze_image(
                    image_url_or_bytes=image_url_or_bytes,
                    prompt=prompt + "\n\n" + GEMINI_NUTRITION_SYSTEM_PROMPT,
                    response_schema=True,
                )
                return self._parse_json_response(raw_json, food_query or "Analyzed Meal")

            # 3. Text or Vision/OCR aggregated data estimation
            prompt_input = food_query or "Balanced Nutritional Meal"
            if vision_ocr_data:
                prompt_input += f" | Vision & OCR Data: {json.dumps(vision_ocr_data)}"

            raw_json = await self.provider.generate_response(
                system_prompt=GEMINI_NUTRITION_SYSTEM_PROMPT,
                prompt=f"Estimate nutrition for: {prompt_input}",
                response_schema=True,
            )
            return self._parse_json_response(raw_json, food_query or "Analyzed Food")

        except Exception as e:
            logger.error("Gemini Nutrition Engine request failed, applying fallback estimation", error=str(e))
            return self._build_fallback_nutrition(food_query, vision_ocr_data)

    def _parse_json_response(self, raw_json: str, default_name: str) -> dict[str, Any]:
        """Parses and validates Gemini JSON output into the standardized nutrition schema."""
        try:
            cleaned = raw_json.strip()
            if cleaned.startswith("```json"):
                cleaned = cleaned[7:]
            if cleaned.startswith("```"):
                cleaned = cleaned[3:]
            if cleaned.endswith("```"):
                cleaned = cleaned[:-3]

            data = json.loads(cleaned.strip())

            return {
                "food_name": str(data.get("food_name", default_name)),
                "estimated_calories": int(data.get("estimated_calories", data.get("calories", 200))),
                "protein_g": round(float(data.get("protein_g", data.get("protein", 10.0))), 1),
                "carbs_g": round(float(data.get("carbs_g", data.get("carbs", 25.0))), 1),
                "fat_g": round(float(data.get("fat_g", data.get("fat", 6.0))), 1),
                "fiber_g": round(float(data.get("fiber_g", 3.0)), 1),
                "sugar_g": round(float(data.get("sugar_g", 4.0)), 1),
                "sodium_mg": round(float(data.get("sodium_mg", 250.0)), 1),
                "serving_size": str(data.get("serving_size", "1 serving")),
                "confidence": round(float(data.get("confidence", 0.90)), 2),
                "reasoning": str(data.get("reasoning", "Estimated via Gemini AI Nutrition Engine.")),
            }
        except Exception as parse_error:
            logger.warning("Failed to parse Gemini JSON output", raw=raw_json, error=str(parse_error))
            return self._build_fallback_nutrition(default_name, None)

    def _build_mock_nutrition(
        self, query: str | None, vision_data: dict[str, Any] | None
    ) -> dict[str, Any]:
        """Generates deterministic mock nutrition values for unit testing and offline development."""
        name = query or "Sample Dish"
        lower_name = name.lower()

        if "apple" in lower_name:
            cals, prot, carbs, fat, fiber = 95, 0.5, 25.0, 0.3, 4.4
        elif "chicken" in lower_name or "protein" in lower_name:
            cals, prot, carbs, fat, fiber = 330, 31.0, 0.0, 3.6, 0.0
        elif "salad" in lower_name:
            cals, prot, carbs, fat, fiber = 150, 4.0, 12.0, 9.0, 5.0
        elif vision_data and "foods" in vision_data:
            cals, prot, carbs, fat, fiber = 450, 18.0, 55.0, 14.0, 6.0
        else:
            cals, prot, carbs, fat, fiber = 380, 12.0, 50.0, 11.0, 7.0

        return {
            "food_name": name.title(),
            "estimated_calories": cals,
            "protein_g": float(prot),
            "carbs_g": float(carbs),
            "fat_g": float(fat),
            "fiber_g": float(fiber),
            "sugar_g": 5.0,
            "sodium_mg": 300.0,
            "serving_size": "1 standard portion (approx 200g)",
            "confidence": 0.92,
            "reasoning": "Mock Gemini AI Nutrition Engine estimation.",
        }

    def _build_fallback_nutrition(
        self, query: str | None, vision_data: dict[str, Any] | None
    ) -> dict[str, Any]:
        """Provides safe fallback estimates if API execution encounters errors."""
        res = self._build_mock_nutrition(query, vision_data)
        res["confidence"] = 0.70
        res["reasoning"] = "Fallback nutrition estimate applied due to API response timeout."
        return res
