from pathlib import Path

import structlog

from src.config.settings import settings
from src.services.vision.interfaces import StorageProvider

logger = structlog.get_logger()


class CloudinaryStorageProvider(StorageProvider):
    """Storage provider implementation for Cloudinary and local mock fallbacks."""

    def __init__(self) -> None:
        self.is_mock = True
        self.cloudinary_url = settings.CLOUDINARY_URL

        # Check if we have a real Cloudinary configuration URL
        if (
            self.cloudinary_url
            and "dev_cloud" not in self.cloudinary_url
            and "dev_key" not in self.cloudinary_url
        ):
            try:
                import cloudinary
                import cloudinary.uploader

                # Automatically reads from CLOUDINARY_URL env/settings
                cloudinary.config(cloudinary_url=self.cloudinary_url)
                self.is_mock = False
                logger.info("Cloudinary storage provider initialized successfully.")
            except ImportError:
                logger.warning(
                    "cloudinary package not installed. Falling back to Mock local uploads."
                )

        if self.is_mock:
            logger.info(
                "Initializing Cloudinary Mock storage provider using local filesystem."
            )
            # Set up local workspace path for uploaded mock images
            self.upload_dir = Path("static/uploads")
            self.upload_dir.mkdir(parents=True, exist_ok=True)

    async def upload_image(self, file_bytes: bytes, filename: str) -> str:
        """Uploads image data to Cloudinary, falling back to writing to local workspace folder.

        Args:
            file_bytes: Raw bytes of the image file.
            filename: Target file name (without extension).

        Returns:
            The public URL of the uploaded image.
        """
        if not self.is_mock:
            try:
                import cloudinary.uploader

                # Cloudinary uploader.upload accepts raw bytes in a stream or file-like object
                response = cloudinary.uploader.upload(
                    file_bytes,
                    public_id=filename,
                    overwrite=True,
                    resource_type="image",
                )
                url = response.get("secure_url")
                if url:
                    logger.info("Successfully uploaded image to Cloudinary", url=url)
                    return str(url)
            except Exception as e:
                logger.error(
                    "Failed to upload to Cloudinary, falling back to local storage",
                    error=str(e),
                )

        # Mock / Local Fallback Upload
        clean_ext = ".jpg"
        if not filename.endswith(clean_ext):
            full_filename = f"{filename}{clean_ext}"
        else:
            full_filename = filename

        local_path = self.upload_dir / full_filename

        # Write bytes locally
        with open(local_path, "wb") as f:
            f.write(file_bytes)

        local_url = f"http://localhost:{settings.PORT}/static/uploads/{full_filename}"
        logger.info(
            "Successfully saved file to mock local storage",
            path=str(local_path),
            url=local_url,
        )
        return local_url
