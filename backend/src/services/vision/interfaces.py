from abc import ABC, abstractmethod
from typing import Any


class StorageProvider(ABC):
    """Abstract interface contract for cloud and local object storage providers."""

    @abstractmethod
    async def upload_image(self, file_bytes: bytes, filename: str) -> str:
        """Uploads raw file bytes to the cloud and returns the public HTTP URL.

        Args:
            file_bytes: The raw image payload in bytes.
            filename: Target file name (e.g. upload uuid).

        Returns:
            The public URL of the uploaded image.
        """
        pass


class VisionProvider(ABC):
    """Abstract interface contract for food identification and portions calculations."""

    @abstractmethod
    async def detect_food(self, image_url: str) -> list[dict[str, Any]]:
        """Identifies food objects detected within the image.

        Args:
            image_url: Publicly accessible URL of the food image.

        Returns:
            A list of dictionary results containing 'label', 'confidence',
            and 'box_coordinates' if available.
        """
        pass

    @abstractmethod
    async def estimate_portion(self, image_url: str, food_item: str) -> dict[str, Any]:
        """Estimates portion sizes, serving quantities, and weights.

        Args:
            image_url: Publicly accessible URL of the food image.
            food_item: Label name of the detected food.

        Returns:
            A dictionary containing portion sizes information (e.g., unit, weight_grams).
        """
        pass


class OCRProvider(ABC):
    """Abstract interface contract for text parsing, labeling, and barcode scanning."""

    @abstractmethod
    async def read_text(self, image_url: str) -> str:
        """Extracts raw text strings from labels, receipts, or menus images.

        Args:
            image_url: Publicly accessible image URL.

        Returns:
            Raw string text extracted from the image.
        """
        pass

    @abstractmethod
    async def parse_nutrition_label(self, image_url: str) -> dict[str, Any]:
        """Parses nutritional value facts from grocery packets nutrition labels.

        Args:
            image_url: Publicly accessible image URL.

        Returns:
            A structured dictionary containing extracted macronutrients (e.g., protein, carbs).
        """
        pass

    @abstractmethod
    async def scan_barcode(self, image_url: str) -> str | None:
        """Extracts and decodes numeric barcode identifiers (EAN/UPC).

        Args:
            image_url: Publicly accessible image URL.

        Returns:
            The barcode digits string if found, otherwise None.
        """
        pass
