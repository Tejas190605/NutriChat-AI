import pytest
from httpx import AsyncClient
from uuid import uuid4
from io import BytesIO
from PIL import Image
from sqlalchemy.ext.asyncio import AsyncSession
from src.services.auth_service import AuthService


@pytest.mark.asyncio
async def test_vision_upload_api_endpoint(client: AsyncClient, db_session: AsyncSession) -> None:
    """Verifies that authenticated users can upload image files to `/api/v1/vision/upload`."""
    if db_session is None:
        pytest.skip("Database is offline")

    # 1. Register and authenticate user
    email = f"vision_user_{uuid4()}@nutrichat.ai"
    password = "secure_password_123"

    auth_service = AuthService(db_session)
    user = await auth_service.register_user(email, password)
    access_token = auth_service.create_access_token(user.id)
    headers = {"Authorization": f"Bearer {access_token}"}

    # 2. Create mock multipart image file
    img = Image.new("RGB", (150, 150), color=(0, 0, 255))
    output = BytesIO()
    img.save(output, format="JPEG")
    img_bytes = output.getvalue()
    
    files = {"file": ("meal_photo.jpg", img_bytes, "image/jpeg")}

    # 3. Post to upload endpoint
    response = await client.post(
        "/api/v1/vision/upload",
        headers=headers,
        files=files,
    )

    # 4. Assertions
    assert response.status_code == 201
    data = response.json()
    assert data["status"] == "success"
    assert "image_id" in data
    assert "image_url" in data
    assert data["image_status"] == "uploaded"


@pytest.mark.asyncio
async def test_vision_upload_unauthorized(client: AsyncClient) -> None:
    """Verifies upload requests without auth tokens are rejected."""
    files = {"file": ("meal.jpg", b"dummy_content", "image/jpeg")}
    response = await client.post("/api/v1/vision/upload", files=files)
    assert response.status_code == 401
