import pytest
import pytest_asyncio
import os
from dotenv import load_dotenv
from unittest.mock import AsyncMock, MagicMock
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy import event

from app.main import app
from app.core.db.base import Base
from app.core.db.database import get_db
from app.core.db import models as _
from app.shared.dependencies.auth import get_current_user_id
from app.modules.restaurants.dependencies import get_restaurant_service
from app.modules.restaurants.services.restaurant import RestaurantService
from app.core.security.jwt_service import jwt_service
from app.modules.users.models import User
from app.modules.restaurants.models import Restaurant

load_dotenv(".env.test", override=True)

db_url = os.getenv("TEST_DATABASE_URL")
assert db_url and "test" in db_url, "NO estás usando la DB de test 💀"

TEST_DATABASE_URL = os.getenv(
    "TEST_DATABASE_URL",
    "postgresql+asyncpg://postgres:postgres@localhost:5432/menu_saas_test"
)

FAKE_USER_ID = 1


# ========== LEGACY FIXTURES (MOCKS) ==========
@pytest.fixture(scope="module")
def mock_restaurant_service():
    service = MagicMock(spec=RestaurantService)
    service.get_all = AsyncMock()
    service.get_by_slug = AsyncMock()
    service.create = AsyncMock()
    service.update = AsyncMock()
    service.delete = AsyncMock()
    return service


@pytest_asyncio.fixture(scope="module")
async def client(mock_restaurant_service):
    app.dependency_overrides[get_current_user_id] = lambda: FAKE_USER_ID
    app.dependency_overrides[get_restaurant_service] = lambda: mock_restaurant_service

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as ac:
        yield ac

    app.dependency_overrides.clear()


# ========== INTEGRATION FIXTURES ==========
@pytest_asyncio.fixture(scope="function")
async def test_db():
    """
    Crea una conexión a la base de datos de prueba.
    Ejecuta las migraciones antes de cada test.
    """
    engine = create_async_engine(TEST_DATABASE_URL, echo=False, pool_pre_ping=True)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    SessionLocal = async_sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )

    async def get_test_db():
        async with SessionLocal() as session:
            try:
                yield session
            except Exception:
                await session.rollback()
                raise
            finally:
                await session.close()

    yield SessionLocal

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await engine.dispose()


@pytest_asyncio.fixture(scope="function")
async def db_session(test_db):
    """Obtiene una sesión de base de datos para usar en tests."""
    SessionLocal = test_db
    async with SessionLocal() as session:
        yield session


@pytest_asyncio.fixture(scope="function")
async def test_user(db_session: AsyncSession) -> User:
    """Crea un usuario de prueba en la base de datos."""
    user = User(
        email="testuser@example.com",
        hashed_password="hashed_password_here"
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    return user


@pytest_asyncio.fixture(scope="function")
async def test_user_jwt_token(test_user: User) -> str:
    """Genera un JWT token válido para el usuario de prueba."""
    return jwt_service.create_access_token(str(test_user.id))


@pytest_asyncio.fixture(scope="function")
async def test_restaurant(db_session: AsyncSession, test_user: User) -> Restaurant:
    """Crea un restaurante de prueba propiedad del usuario de prueba."""
    restaurant = Restaurant(
        owner_id=test_user.id,
        name="Test Restaurant",
        slug="test-restaurant",
        description="A test restaurant",
        logo_url=None,
        settings={"theme": "light"}
    )
    db_session.add(restaurant)
    await db_session.commit()
    await db_session.refresh(restaurant)
    return restaurant


@pytest_asyncio.fixture(scope="function")
async def integration_client(test_db):
    """
    Cliente HTTP preparado para tests de integración con BD real.
    Overridea las dependencias para usar la BD de prueba.
    """
    SessionLocal = test_db

    async def override_get_db():
        async with SessionLocal() as session:
            try:
                yield session
            except Exception:
                await session.rollback()
                raise

    # Override del get_current_user_id que valida JWT correctamente
    async def override_get_current_user_id(credentials):
        """Valida el JWT y retorna el user_id"""
        try:
            payload = jwt_service.verify_access_token(credentials.credentials)
            return int(payload.sub)
        except ValueError:
            from app.core.exceptions import UnauthorizedException
            raise UnauthorizedException("Invalid or expired token")

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_current_user_id] = override_get_current_user_id

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://testserver",
    ) as ac:
        yield ac

    app.dependency_overrides.clear()