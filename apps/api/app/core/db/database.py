from typing import AsyncGenerator
from sqlalchemy import create_engine, URL
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from app.core.config import settings

def _make_url(driver: str) -> URL:
    return URL.create(
        drivername=f"{settings.db_motor}+{driver}",
        username=settings.db_user,
        password=settings.db_password,
        host=settings.db_host,
        port=settings.db_port,
        database=settings.db_name,
    )

# --- Async (para la app) ---
async_engine = create_async_engine(
    _make_url(settings.db_driver_async),
    echo=False,
    pool_pre_ping=True,
)

AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise

# --- Sync (para Alembic) ---
sync_engine = create_engine(
    _make_url(settings.db_driver_sync),
    echo=False,
    pool_pre_ping=True,
)