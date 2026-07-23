from typing import Any

from src.services.vision.interfaces import OCRProvider, VisionProvider


class MockVisionProvider(VisionProvider):
    """Mock implementation of the VisionProvider interface returning predefined structures."""

    async def detect_food(self, image_url: str) -> list[dict[str, Any]]:
        """Mock identifies a food dish based on the image URL keywords."""
        if "apple" in image_url.lower():
            return [
                {
                    "label": "Apple",
                    "confidence": 0.9850,
                    "box_coordinates": {
                        "ymin": 10,
                        "xmin": 12,
                        "ymax": 120,
                        "xmax": 125,
                    },
                }
            ]
        elif "salad" in image_url.lower():
            return [
                {
                    "label": "Green Salad",
                    "confidence": 0.9400,
                    "box_coordinates": {
                        "ymin": 50,
                        "xmin": 50,
                        "ymax": 400,
                        "xmax": 450,
                    },
                }
            ]

        # Default mock fallback
        return [
            {
                "label": "Roti Paneer",
                "confidence": 0.9100,
                "box_coordinates": {"ymin": 100, "xmin": 100, "ymax": 350, "xmax": 350},
            }
        ]

    async def estimate_portion(self, _image_url: str, food_item: str) -> dict[str, Any]:
        """Mock estimates portions sizes."""
        if "apple" in food_item.lower():
            return {"unit": "piece", "weight_grams": 182.0, "quantity": 1.0}
        elif "salad" in food_item.lower():
            return {"unit": "bowl", "weight_grams": 200.0, "quantity": 1.0}

        return {"unit": "serving", "weight_grams": 250.0, "quantity": 1.0}


class MockOCRProvider(OCRProvider):
    """Mock implementation of the OCRProvider interface returning label texts & codes."""

    async def read_text(self, _image_url: str) -> str:
        """Returns standard nutrition label plaintext contents."""
        return "Nutrition Facts Serving Size 1 pack Calories 230 Total Fat 8g Protein 10g Total Carbs 30g"

    async def parse_nutrition_label(self, _image_url: str) -> dict[str, Any]:
        """Extracts structured nutritional stats."""
        return {
            "calories": 230,
            "protein": 10.0,
            "carbs": 30.0,
            "fat": 8.0,
            "sodium_mg": 160.0,
        }

    async def scan_barcode(self, image_url: str) -> str | None:
        """Returns a scanned numeric code based on URL hints."""
        if "fail" in image_url.lower():
            return None
        return "8901234567890"
