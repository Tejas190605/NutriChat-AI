from io import BytesIO

import pytest
from PIL import Image

from src.services.vision.preprocessing import preprocess_image


def test_image_preprocessing_resizing_and_compression() -> None:
    """Verifies that large raw image bytes are correctly resized and compressed."""
    # 1. Create a dummy test image in memory (RGBA format, 1200x900 pixels)
    img = Image.new("RGBA", (1200, 900), color=(255, 0, 0, 255))
    output_io = BytesIO()
    img.save(output_io, format="PNG")
    raw_png_bytes = output_io.getvalue()

    # 2. Preprocess raw PNG bytes
    processed_bytes = preprocess_image(raw_png_bytes, max_size=(800, 800), quality=85)

    # 3. Assertions
    processed_img = Image.open(BytesIO(processed_bytes))
    assert processed_img.format == "JPEG"
    assert processed_img.mode == "RGB"

    # Aspect ratio validation: 1200x900 -> ratio 4:3. Max dimension 800.
    # New size should be 800x600.
    assert processed_img.size == (800, 600)
    # Verify output size is small (under 50 KB)
    assert len(processed_bytes) < 50_000


def test_image_preprocessing_format_validation() -> None:
    """Verifies that unsupported file content raises ValueError."""
    # Invalid file contents
    bad_bytes = b"not_an_image_file_executable_contents"
    with pytest.raises(ValueError, match="Corrupted or invalid image binary payload"):
        preprocess_image(bad_bytes)
