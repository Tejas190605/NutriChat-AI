"""Unit tests for Settings configuration, CORS_ORIGINS parsing, and production environment loading."""

import json

from src.config.settings import Settings


def test_cors_origins_parsing_from_json_string() -> None:
    """Verifies CORS_ORIGINS parses a valid JSON array string."""
    json_origins = json.dumps(["https://nutrichat-frontend.onrender.com", "http://localhost:3000"])
    settings = Settings(CORS_ORIGINS=json_origins)

    assert settings.CORS_ORIGINS == [
        "https://nutrichat-frontend.onrender.com",
        "http://localhost:3000",
    ]


def test_cors_origins_parsing_from_single_raw_url_string() -> None:
    """Verifies CORS_ORIGINS parses a single raw URL string from Render RENDER_EXTERNAL_URL."""
    raw_url = "https://nutrichat-frontend.onrender.com"
    settings = Settings(CORS_ORIGINS=raw_url)

    assert settings.CORS_ORIGINS == ["https://nutrichat-frontend.onrender.com"]


def test_cors_origins_parsing_from_comma_separated_string() -> None:
    """Verifies CORS_ORIGINS parses comma-separated origin strings."""
    comma_origins = "https://admin.nutrichat.ai, https://app.nutrichat.ai"
    settings = Settings(CORS_ORIGINS=comma_origins)

    assert settings.CORS_ORIGINS == [
        "https://admin.nutrichat.ai",
        "https://app.nutrichat.ai",
    ]


def test_cors_origins_parsing_from_list() -> None:
    """Verifies CORS_ORIGINS accepts standard list of strings."""
    list_origins = ["http://localhost:3000", "http://127.0.0.1:3000"]
    settings = Settings(CORS_ORIGINS=list_origins)

    assert settings.CORS_ORIGINS == list_origins


def test_cors_origins_fallback_on_empty_string() -> None:
    """Verifies CORS_ORIGINS falls back to default origins on empty or whitespace strings."""
    settings = Settings(CORS_ORIGINS="   ")
    assert settings.CORS_ORIGINS == ["http://localhost:3000", "http://127.0.0.1:3000"]


def test_production_settings_initialization(monkeypatch) -> None:
    """Verifies Settings initializes cleanly under production environment variables without SettingsError."""
    monkeypatch.setenv("ENV", "production")
    monkeypatch.setenv("DEBUG", "false")
    monkeypatch.setenv("CORS_ORIGINS", "https://nutrichat-frontend.onrender.com")
    monkeypatch.setenv("POSTGRES_USER", "prod_user")
    monkeypatch.setenv("POSTGRES_PASSWORD", "prod_password")
    monkeypatch.setenv("POSTGRES_HOST", "prod-db-host")
    monkeypatch.setenv("POSTGRES_PORT", "5432")
    monkeypatch.setenv("POSTGRES_DB", "nutrichat_prod")

    prod_settings = Settings()

    assert prod_settings.ENV == "production"
    assert prod_settings.DEBUG is False
    assert prod_settings.CORS_ORIGINS == ["https://nutrichat-frontend.onrender.com"]
    assert "prod_user" in prod_settings.DATABASE_URL
    assert "prod-db-host" in prod_settings.DATABASE_URL
