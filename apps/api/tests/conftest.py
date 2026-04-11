import pytest
import pytest_asyncio
from unittest.mock import AsyncMock, MagicMock
from httpx import AsyncClient, ASGITransport

from app.main import app
from app.shared.dependencies.auth import get_current_user_id
from app.modules.restaurants.dependencies import get_restaurant_service
from app.modules.restaurants.services.restaurant import RestaurantService

FAKE_USER_ID = 1


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