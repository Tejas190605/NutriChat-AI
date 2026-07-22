from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.token import RefreshToken
from src.repositories.base import BaseRepository


class RefreshTokenRepository(BaseRepository[RefreshToken]):
    """Specific repository for RefreshToken-related database operations."""

    def __init__(self, db: AsyncSession):
        super().__init__(RefreshToken, db)

    async def get_by_token(self, token: str) -> RefreshToken | None:
        """Finds a refresh token by its unique string hash."""
        result = await self.db.execute(
            select(self.model).filter(self.model.token == token)
        )
        return result.scalars().first()
