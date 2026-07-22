from pydantic import BaseModel, EmailStr, Field


class UserRegisterRequest(BaseModel):
    """Pydantic model representing registration request body payload."""

    email: EmailStr = Field(..., description="User email address")
    password: str = Field(
        ..., min_length=8, max_length=100, description="User password"
    )


class UserLoginRequest(BaseModel):
    """Pydantic model representing login credentials request body payload."""

    email: EmailStr = Field(..., description="User email address")
    password: str = Field(..., description="User password")


class TokenResponse(BaseModel):
    """Pydantic model representing JWT access and refresh token responses."""

    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenRefreshRequest(BaseModel):
    """Pydantic model representing token rotation refresh requests."""

    refresh_token: str
