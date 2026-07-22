import uuid
from datetime import UTC, datetime, timedelta
from uuid import UUID

import jwt
import structlog
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from sqlalchemy.ext.asyncio import AsyncSession

from src.config.settings import settings
from src.models.audit import AuditLog
from src.models.session import UserSession
from src.models.user import User
from src.repositories.base import BaseRepository
from src.repositories.token import RefreshTokenRepository
from src.repositories.user import UserRepository

logger = structlog.get_logger()
ph = PasswordHasher()


class AuthService:
    """Business service orchestrating password security, JWT operations, and audit logs."""

    def __init__(self, db: AsyncSession):
        self.db = db
        self.user_repo = UserRepository(db)
        self.token_repo = RefreshTokenRepository(db)
        self.session_repo = BaseRepository(UserSession, db)
        self.audit_repo = BaseRepository(AuditLog, db)

    def hash_password(self, password: str) -> str:
        """Hashes a password string using the Argon2 hashing algorithm."""
        return ph.hash(password)

    def verify_password(self, hashed_password: str, password: str) -> bool:
        """Verifies a plain password string against an Argon2 hash."""
        try:
            return ph.verify(hashed_password, password)
        except VerifyMismatchError:
            return False
        except Exception as e:
            logger.error("Password verification error occurred", error=str(e))
            return False

    async def register_user(self, email: str, password: str) -> User:
        """Registers a new user inside the system, hashing their password."""
        existing_user = await self.user_repo.get_by_email(email)
        if existing_user:
            raise ValueError("User with this email already registered")

        hashed_password = self.hash_password(password)
        user = await self.user_repo.create(
            {
                "email": email,
                "hashed_password": hashed_password,
                "is_active": True,
                "is_superuser": False,
            }
        )
        return user

    async def authenticate_user(self, email: str, password: str) -> User | None:
        """Authenticates a user email and password."""
        user = await self.user_repo.get_by_email(email)
        if not user or not user.is_active:
            return None
        if self.verify_password(user.hashed_password, password):
            return user
        return None

    def create_access_token(self, user_id: UUID) -> str:
        """Generates a short-lived JWT access token."""
        now = datetime.now(UTC)
        expire = now + timedelta(minutes=30)
        payload = {
            "sub": str(user_id),
            "exp": int(expire.timestamp()),
            "iat": int(now.timestamp()),
            "type": "access",
        }
        return jwt.encode(
            payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM
        )

    async def create_refresh_token(self, user_id: UUID) -> str:
        """Generates a long-lived refresh token and stores it in the database."""
        now = datetime.now(UTC)
        expire = now + timedelta(
            hours=settings.JWT_EXPIRATION_HOURS * 24
        )  # Expire in days config
        payload = {
            "sub": str(user_id),
            "exp": int(expire.timestamp()),
            "iat": int(now.timestamp()),
            "type": "refresh",
            "jti": str(uuid.uuid4()),  # Unique token ID
        }
        token_str = jwt.encode(
            payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM
        )

        # Save token model in database
        await self.token_repo.create(
            {
                "user_id": user_id,
                "token": token_str,
                "is_revoked": False,
                "expires_at": expire,
            }
        )
        return token_str

    async def rotate_tokens(self, refresh_token_str: str) -> tuple[str, str]:
        """Rotates a refresh token, validating signatures and issuing a new set."""
        try:
            payload = jwt.decode(
                refresh_token_str,
                settings.JWT_SECRET,
                algorithms=[settings.JWT_ALGORITHM],
            )
            if payload.get("type") != "refresh":
                raise ValueError("Invalid token type")
        except jwt.PyJWTError as e:
            raise ValueError("Invalid refresh token signature") from e

        # Load token record from database
        token_record = await self.token_repo.get_by_token(refresh_token_str)
        if (
            not token_record
            or token_record.is_revoked
            or token_record.expires_at.replace(tzinfo=UTC) < datetime.now(UTC)
        ):
            raise ValueError("Refresh token is expired, revoked, or untracked")

        # Revoke old refresh token
        token_record.is_revoked = True
        self.db.add(token_record)

        # Issue new token pair
        user_id = UUID(payload["sub"])
        new_access = self.create_access_token(user_id)
        new_refresh = await self.create_refresh_token(user_id)

        return new_access, new_refresh

    async def revoke_token(self, refresh_token_str: str) -> None:
        """Revokes a refresh token string, disabling further rotations."""
        token_record = await self.token_repo.get_by_token(refresh_token_str)
        if token_record:
            token_record.is_revoked = True
            self.db.add(token_record)

    async def create_user_session(
        self, user_id: UUID, user_agent: str | None, ip_address: str | None
    ) -> UserSession:
        """Creates a session logging record for an active user login."""
        now = datetime.now(UTC)
        expire = now + timedelta(hours=settings.JWT_EXPIRATION_HOURS)
        session = await self.session_repo.create(
            {
                "user_id": user_id,
                "user_agent": user_agent,
                "ip_address": ip_address,
                "is_active": True,
                "expires_at": expire,
            }
        )
        return session

    async def log_audit(
        self,
        user_id: UUID | None,
        action: str,
        ip_address: str | None,
        details: str | None,
    ) -> AuditLog:
        """Logs an administrative activity to the database audit trail."""
        log = await self.audit_repo.create(
            {
                "user_id": user_id,
                "action": action,
                "ip_address": ip_address,
                "details": details,
            }
        )
        return log
