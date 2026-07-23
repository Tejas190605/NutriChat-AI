from io import BytesIO

import structlog
from PIL import Image

logger = structlog.get_logger()


def preprocess_image(
    file_bytes: bytes,
    max_size: tuple[int, int] = (800, 800),
    quality: int = 85,
) -> bytes:
    """Validates image structure, resizes down to maximum constraints, and compresses to JPEG.

    Args:
        file_bytes: Raw binary payload of the image upload.
        max_size: Max width and height dimensions constraint.
        quality: Compression ratio from 1 to 100.

    Returns:
        Compressed JPEG binary payload.

    Raises:
        ValueError: If image format is invalid or corrupted.
    """
    try:
        img: Image.Image = Image.open(BytesIO(file_bytes))

        # Verify it's a supported format
        if img.format not in ("JPEG", "PNG", "WEBP", "MPO", "BMP"):
            raise ValueError(f"Unsupported image format type: {img.format}")

        # Apply resizing keeping aspect ratio
        img.thumbnail(max_size, Image.Resampling.LANCZOS)

        # Ensure image is converted to RGB mode to support saving as JPEG
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")

        output = BytesIO()
        img.save(output, format="JPEG", quality=quality)
        compressed_bytes = output.getvalue()

        logger.info(
            "Image preprocessed successfully",
            original_size_kb=round(len(file_bytes) / 1024, 2),
            compressed_size_kb=round(len(compressed_bytes) / 1024, 2),
        )
        return compressed_bytes

    except Exception as e:
        if isinstance(e, ValueError):
            raise e
        raise ValueError(f"Corrupted or invalid image binary payload: {str(e)}") from e
