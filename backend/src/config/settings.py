import json
from typing import Any

from pydantic import Field, field_validator, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    APP_NAME: str = Field(default="NutriChat-AI")
    ENV: str = Field(default="development")
    DEBUG: bool = Field(default=True)
    PORT: int = Field(default=8000)
    CORS_ORIGINS: list[str] = Field(
        default=["http://localhost:3000", "http://127.0.0.1:3000"]
    )

    @field_validator("CORS_ORIGINS", mode="before")
    @classmethod
    def parse_cors_origins(cls, v: Any) -> list[str]:
        """Parses CORS_ORIGINS safely from JSON arrays, single raw URL strings, or comma-separated strings."""
        if isinstance(v, list):
            return [str(item).strip() for item in v if str(item).strip()]
        if isinstance(v, str):
            v_trimmed = v.strip()
            if not v_trimmed:
                return ["http://localhost:3000", "http://127.0.0.1:3000"]
            if v_trimmed.startswith("[") and v_trimmed.endswith("]"):
                try:
                    parsed = json.loads(v_trimmed)
                    if isinstance(parsed, list):
                        return [str(item).strip() for item in parsed if str(item).strip()]
                except json.JSONDecodeError:
                    pass
            origins = [item.strip() for item in v_trimmed.split(",") if item.strip()]
            return origins if origins else ["http://localhost:3000", "http://127.0.0.1:3000"]
        return v

    # Database
    POSTGRES_USER: str = Field(default="postgres")
    POSTGRES_PASSWORD: str = Field(default="postgres")
    POSTGRES_HOST: str = Field(default="localhost")
    POSTGRES_PORT: int = Field(default=5432)
    POSTGRES_DB: str = Field(default="nutrichat")
    DATABASE_URL: str = Field(
        default="postgresql+asyncpg://postgres:postgres@localhost:5432/nutrichat"
    )

    # Redis and Celery
    REDIS_URL: str = Field(default="redis://localhost:6379/0")
    CELERY_BROKER_URL: str = Field(default="redis://localhost:6379/1")
    CELERY_RESULT_BACKEND: str = Field(default="redis://localhost:6379/2")

    # Security
    JWT_SECRET: str = Field(default="dev_jwt_secret_token")
    JWT_ALGORITHM: str = Field(default="HS256")
    JWT_EXPIRATION_HOURS: int = Field(default=2)

    # Webhook Verification
    FACEBOOK_APP_SECRET: str = Field(default="dev_facebook_app_secret")
    FACEBOOK_VERIFY_TOKEN: str = Field(default="dev_facebook_verify_token")
    WHATSAPP_PHONE_NUMBER_ID: str = Field(default="dev_phone_number_id")
    WHATSAPP_ACCESS_TOKEN: str = Field(default="dev_whatsapp_access_token")

    # AI & Media Storage APIs
    GEMINI_API_KEY: str = Field(default="dev_gemini_key")
    CLOUDINARY_URL: str = Field(default="cloudinary://dev_key:dev_secret@dev_cloud")

    @model_validator(mode="after")
    def assemble_db_url(self) -> "Settings":
        # Assemble fallback database URL if default is not custom
        if (
            not self.DATABASE_URL
            or self.DATABASE_URL
            == "postgresql+asyncpg://postgres:postgres@localhost:5432/nutrichat"
        ):
            self.DATABASE_URL = f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        return self


# Global single instance of settings
settings = Settings()
