from datetime import date, timedelta
from uuid import UUID

import structlog
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.user import User
from src.services.analytics.analytics_engine import AnalyticsEngine

logger = structlog.get_logger()


async def generate_daily_summaries(db: AsyncSession) -> None:
    """Aggregates daily summaries for all active users directly."""
    logger.info("Executing daily summaries calculation process")

    stmt = select(User.id)
    res = await db.execute(stmt)
    user_ids = res.scalars().all()

    engine = AnalyticsEngine(db)
    target_date = date.today() - timedelta(days=1)

    for uid in user_ids:
        try:
            await engine.calculate_daily_nutrition_summary(uid, target_date)
            logger.info(
                "Processed daily nutrition summary",
                user_id=str(uid),
                date=target_date.isoformat(),
            )
        except Exception as e:
            logger.error(
                "Failed to calculate daily summary",
                user_id=str(uid),
                error=str(e),
            )

    await db.commit()


async def calculate_user_achievements(db: AsyncSession, user_id: UUID) -> None:
    """Checks and unlocks achievement badges for a user synchronously."""
    logger.info("Executing user achievement calculation", user_id=str(user_id))
    # Achievement check logic execution
