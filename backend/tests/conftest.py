import asyncio
from collections.abc import AsyncGenerator, Generator
import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from src.config.settings import settings
from src.db.session import get_async_session
from src.db.base import Base
from src.main import app

# Create isolated test database engine
test_engine = create_async_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
)

TestingSessionLocal = async_sessionmaker(
    bind=test_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


@pytest.fixture(scope="session")
def event_loop() -> Generator[asyncio.AbstractEventLoop, None, None]:
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(autouse=True)
async def init_test_db() -> AsyncGenerator[None, None]:
    """Initializes schema tables in test database database."""
    has_db = False
    try:
        async with test_engine.begin() as conn:
            # Create all tables matching Base declarations
            await conn.run_sync(Base.metadata.create_all)
        has_db = True
    except Exception:
        print("\n[Warning] Test Database is offline. Skipping schema initializations.")
        
    yield
    
    if has_db:
        try:
            async with test_engine.begin() as conn:
                # Drop all tables after test session ends
                await conn.run_sync(Base.metadata.drop_all)
        except Exception:
            pass


@pytest.fixture
async def db_session() -> AsyncGenerator[AsyncSession | None, None]:
    """Yields an isolated async session for database queries assertions."""
    try:
        async with TestingSessionLocal() as session:
            yield session
            await session.rollback()
            await session.close()
    except Exception:
        yield None


@pytest.fixture
async def client(db_session: AsyncSession | None) -> AsyncGenerator[AsyncClient, None]:
    """Async HTTP Client fixture wrapping FastAPI, with overridden DB dependencies."""
    
    async def override_get_async_session() -> AsyncGenerator[AsyncSession | None, None]:
        yield db_session

    app.dependency_overrides[get_async_session] = override_get_async_session
    
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac
        
    app.dependency_overrides.clear()
