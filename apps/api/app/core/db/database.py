from typing import AsyncGenerator
import ssl
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from app.core.config import settings


def get_async_connect_args() -> dict:
    if settings.environment == "production":
        ssl_context = ssl.create_default_context()
        return {"ssl": ssl_context}
    return {}


def get_sync_connect_args() -> dict:
    if settings.environment == "production":
        return {"sslmode": "require"}
    return {}


# --- Async (App) ---
async_engine = create_async_engine(
    settings.db_url,
    echo=settings.environment == "development",
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10,
    connect_args=get_async_connect_args(),
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


# --- Sync (Alembic) ---
sync_db_url = settings.db_url.replace("+asyncpg", "")

sync_engine = create_engine(
    sync_db_url,
    echo=False,
    pool_pre_ping=True,
    connect_args=get_sync_connect_args(),
)