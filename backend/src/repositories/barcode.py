from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from src.models.barcode import BarcodeProduct
from src.repositories.base import BaseRepository


class BarcodeRepository(BaseRepository[BarcodeProduct]):
    """Repository for BarcodeProduct lookups."""

    def __init__(self, db: AsyncSession):
        super().__init__(BarcodeProduct, db)

    async def get_by_barcode(self, barcode: str) -> BarcodeProduct | None:
        """Finds a product matching a scanned barcode value, preloading nutrients."""
        stmt = (
            select(self.model)
            .filter(self.model.barcode == barcode)
            .options(joinedload(BarcodeProduct.nutrition_fact))
        )
        res = await self.db.execute(stmt)
        return res.scalars().first()
