import asyncio
from datetime import date, timedelta

import structlog
from sqlalchemy import select

from src.db.session import AsyncSessionLocal
from src.models.user import User
from src.services.analytics.analytics_engine import AnalyticsEngine
from src.services.celery_app import celery_app

logger = structlog.get_logger()


@celery_app.task(
    name="src.services.analytics.tasks.daily_summaries_generation_task"
)  # type: ignore[untyped-decorator]
def daily_summaries_generation_task() -> None:
    """Cron-triggered task to aggregate daily summaries for all active users."""
    logger.info("Executing Celery daily summaries calculation task")

    async def _process() -> None:
        async with AsyncSessionLocal() as session:
            # Fetch all user IDs
            stmt = select(User.id)
            res = await session.execute(stmt)
            user_ids = res.scalars().all()

            engine = AnalyticsEngine(session)
            target_date = date.today() - timedelta(days=1)  # Process yesterday's logs

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
                        "Failed to calculate daily summaries",
                        user_id=str(uid),
                        error=str(e),
                    )

            await session.commit()

    loop = asyncio.get_event_loop()
    if loop.is_running():
        asyncio.ensure_future(_process())
    else:
        loop.run_until_complete(_process())


@celery_app.task(
    name="src.services.analytics.tasks.achievement_calculation_task"
)  # type: ignore[untyped-decorator]
def achievement_calculation_task(user_id_str: str) -> None:
    """Asynchronous task triggered to check and unlock achievements badges for a user."""
    logger.info("Executing Celery achievement calculation task", user_id=user_id_str)
    # Mock behavior for achievement check checks
