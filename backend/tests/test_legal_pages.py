"""Automated tests for public legal pages required by Meta WhatsApp Cloud API publishing."""

import pytest
from httpx import AsyncClient

REAL_SUPPORT_EMAIL = "tejasawant1962005@gmail.com"
FAKE_SUPPORT_EMAIL = "support@nutrichat.ai"


@pytest.mark.asyncio
async def test_privacy_policy_page(client: AsyncClient) -> None:
    """Verifies GET /privacy returns HTTP 200 HTML page with expected Privacy Policy content."""
    response = await client.get("/privacy")

    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"].lower()
    assert "Privacy Policy" in response.text
    assert "NutriChat AI" in response.text
    assert REAL_SUPPORT_EMAIL in response.text
    assert FAKE_SUPPORT_EMAIL not in response.text
    assert f"mailto:{REAL_SUPPORT_EMAIL}" in response.text
    assert "/terms" in response.text
    assert "/data-deletion" in response.text


@pytest.mark.asyncio
async def test_terms_of_service_page(client: AsyncClient) -> None:
    """Verifies GET /terms returns HTTP 200 HTML page with expected Terms of Service content."""
    response = await client.get("/terms")

    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"].lower()
    assert "Terms of Service" in response.text
    assert "Medical" in response.text or "Disclaimer" in response.text
    assert REAL_SUPPORT_EMAIL in response.text
    assert FAKE_SUPPORT_EMAIL not in response.text
    assert f"mailto:{REAL_SUPPORT_EMAIL}" in response.text
    assert "/privacy" in response.text
    assert "/data-deletion" in response.text


@pytest.mark.asyncio
async def test_data_deletion_page(client: AsyncClient) -> None:
    """Verifies GET /data-deletion returns HTTP 200 HTML page with accurate deletion instructions."""
    response = await client.get("/data-deletion")

    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"].lower()
    assert "Data Deletion" in response.text
    assert REAL_SUPPORT_EMAIL in response.text
    assert FAKE_SUPPORT_EMAIL not in response.text
    assert f"mailto:{REAL_SUPPORT_EMAIL}" in response.text

    # Assert /reset is clarified as session reset rather than complete account deletion
    assert "does not constitute a complete account" in response.text.lower()
    assert "Resetting Your WhatsApp Session" in response.text
    assert "Request Complete Data Deletion" in response.text

    # Navigation links check
    assert "/privacy" in response.text
    assert "/terms" in response.text
