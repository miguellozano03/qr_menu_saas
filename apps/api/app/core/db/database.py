from typing import AsyncGenerator
import ssl
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from app.core.config import settings

ssl_context = ssl.create_default_context()

# --- Async (App) ---
async_engine = create_async_engine(
    settings.db_url,
    echo=False,
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10,
    connect_args={"ssl": ssl_context},
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
    connect_args={"sslmode": "require"}
)