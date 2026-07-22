from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.models.user import User
from src.repositories.base import BaseRepository


class UserRepository(BaseRepository[User]):
    """Specific repository for User-related database operations."""

    def __init__(self, db: AsyncSession):
        super().__init__(User, db)

    async def get_by_email(self, email: str) -> User | None:
        """Finds a user by their unique email address."""
        query = select(self.model).filter(self.model.email == email)
        if hasattr(self.model, "deleted_at"):
            query = query.filter(self.model.deleted_at.is_(None))
        result = await self.db.execute(query)
        return result.scalars().first()

    async def get_with_profile(self, id: UUID) -> User | None:
        """Finds a user by id and eager loads their 1-to-1 profile."""
        query = (
            select(self.model)
            .filter(self.model.id == id)
            .options(selectinload(User.profile))
        )
        if hasattr(self.model, "deleted_at"):
            query = query.filter(self.model.deleted_at.is_(None))
        result = await self.db.execute(query)
        return result.scalars().first()
