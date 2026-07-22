from typing import Any, Generic, TypeVar
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.base import Base

ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    """Generic base repository defining standard asynchronous database operations."""

    def __init__(self, model: type[ModelType], db: AsyncSession):
        self.model = model
        self.db = db

    async def get(self, id: UUID) -> ModelType | None:
        """Retrieves a single model entity by its primary UUID key, ignoring soft deleted ones."""
        query = select(self.model).filter(self.model.id == id)  # type: ignore[attr-defined]
        if hasattr(self.model, "deleted_at"):
            query = query.filter(self.model.deleted_at.is_(None))  # type: ignore[attr-defined]
        result = await self.db.execute(query)
        return result.scalars().first()

    async def get_multi(self, *, skip: int = 0, limit: int = 100) -> list[ModelType]:
        """Retrieves a list of model entities with pagination offsets, ignoring soft deleted ones."""
        query = select(self.model)
        if hasattr(self.model, "deleted_at"):
            query = query.filter(self.model.deleted_at.is_(None))  # type: ignore[attr-defined]
        result = await self.db.execute(query.offset(skip).limit(limit))
        return list(result.scalars().all())

    async def create(self, obj_in: dict[str, Any] | ModelType) -> ModelType:
        """Inserts a new model instance into the database session."""
        if isinstance(obj_in, dict):
            db_obj = self.model(**obj_in)
        else:
            db_obj = obj_in
        self.db.add(db_obj)
        await self.db.flush()
        return db_obj

    async def update(self, db_obj: ModelType, obj_in: dict[str, Any]) -> ModelType:
        """Updates attributes of an active database model instance."""
        for field, value in obj_in.items():
            if hasattr(db_obj, field):
                setattr(db_obj, field, value)
        self.db.add(db_obj)
        await self.db.flush()
        return db_obj

    async def remove(self, id: UUID) -> ModelType | None:
        """Removes a model instance, performing a soft delete if supported."""
        db_obj = await self.get(id)
        if db_obj:
            if hasattr(db_obj, "deleted_at"):
                from datetime import UTC, datetime

                db_obj.deleted_at = datetime.now(UTC)
                self.db.add(db_obj)
            else:
                await self.db.delete(db_obj)
            await self.db.flush()
        return db_obj
