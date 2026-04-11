import pytest
from app.core.exceptions import ResourceNotFoundException, IsDuplicatedException

BASE = "/v1/restaurants"

def make_restaurant(id: int = 1, name: str = "La Hamburguesería") -> dict:
    return {
        "id": id,
        "name": name,
        "slug": "la-hamburgueseria",
        "description": "La mejor hamburguesa de la ciudad",
        "logo_url": None,
        "settings": None,
    }


VALID_CREATE = {
    "name": "La Hamburguesería",
    "description": "La mejor hamburguesa de la ciudad",
    "logo_url": None,
    "settings": None,
}

VALID_UPDATE = {"name": "La Hamburguesería 2.0"}


# ---------------------------------------------------------------------------
# GET /v1/restaurants
# ---------------------------------------------------------------------------

async def test_get_restaurants_returns_list(client, mock_restaurant_service):
    mock_restaurant_service.get_all.return_value = [make_restaurant()]

    response = await client.get(BASE)

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert data[0]["slug"] == "la-hamburgueseria"
    mock_restaurant_service.get_all.assert_awaited_once_with(
        user_id=1, limit=10, offset=0
    )


async def test_get_restaurants_with_pagination(client, mock_restaurant_service):
    mock_restaurant_service.get_all.reset_mock()
    mock_restaurant_service.get_all.return_value = []

    response = await client.get(BASE, params={"limit": 5, "offset": 10})

    assert response.status_code == 200
    assert response.json() == []
    mock_restaurant_service.get_all.assert_awaited_once_with(
        user_id=1, limit=5, offset=10
    )


# ---------------------------------------------------------------------------
# GET /v1/restaurants/{slug}
# ---------------------------------------------------------------------------

async def test_get_restaurant_by_slug_found(client, mock_restaurant_service):
    mock_restaurant_service.get_by_slug.reset_mock()
    mock_restaurant_service.get_by_slug.return_value = make_restaurant()

    response = await client.get(f"{BASE}/la-hamburgueseria")

    assert response.status_code == 200
    assert response.json()["slug"] == "la-hamburgueseria"
    mock_restaurant_service.get_by_slug.assert_awaited_once_with(
        slug="la-hamburgueseria", user_id=1
    )


async def test_get_restaurant_by_slug_not_found(client, mock_restaurant_service):
    mock_restaurant_service.get_by_slug.reset_mock()
    mock_restaurant_service.get_by_slug.side_effect = ResourceNotFoundException(
        "Restaurant not found"
    )

    response = await client.get(f"{BASE}no-existe")

    assert response.status_code == 404
    mock_restaurant_service.get_by_slug.side_effect = None


# ---------------------------------------------------------------------------
# POST /v1/restaurants
# ---------------------------------------------------------------------------

async def test_create_restaurant_success(client, mock_restaurant_service):
    mock_restaurant_service.create.reset_mock()
    mock_restaurant_service.create.return_value = make_restaurant()

    response = await client.post(BASE, json=VALID_CREATE)

    assert response.status_code == 200
    assert response.json()["id"] == 1
    assert response.json()["name"] == "La Hamburguesería"
    mock_restaurant_service.create.assert_awaited_once()


async def test_create_restaurant_duplicate_slug(client, mock_restaurant_service):
    mock_restaurant_service.create.reset_mock()
    mock_restaurant_service.create.side_effect = IsDuplicatedException(
        "A restaurant with this slug already exists"
    )

    response = await client.post(BASE, json=VALID_CREATE)

    assert response.status_code == 409
    mock_restaurant_service.create.side_effect = None


async def test_create_restaurant_invalid_body(client, mock_restaurant_service):
    """Pydantic rechaza el body antes de llegar al servicio (name vacío falla min_length=1)."""
    mock_restaurant_service.create.reset_mock()

    response = await client.post(BASE, json={"name": ""})

    assert response.status_code == 422
    mock_restaurant_service.create.assert_not_awaited()


# ---------------------------------------------------------------------------
# PATCH /v1/restaurants/{restaurant_id}
# ---------------------------------------------------------------------------

async def test_update_restaurant_success(client, mock_restaurant_service):
    mock_restaurant_service.update.reset_mock()
    mock_restaurant_service.update.return_value = make_restaurant(name="La Hamburguesería 2.0")

    response = await client.patch(f"{BASE}/1", json=VALID_UPDATE)

    assert response.status_code == 200
    assert response.json()["name"] == "La Hamburguesería 2.0"
    mock_restaurant_service.update.assert_awaited_once_with(
        restaurant_id=1, user_id=1, data=mock_restaurant_service.update.call_args.kwargs["data"]
    )


async def test_update_restaurant_not_found(client, mock_restaurant_service):
    mock_restaurant_service.update.reset_mock()
    mock_restaurant_service.update.side_effect = ResourceNotFoundException(
        "Restaurant not found"
    )

    response = await client.patch(f"{BASE}/99", json=VALID_UPDATE)

    assert response.status_code == 404
    mock_restaurant_service.update.side_effect = None


# ---------------------------------------------------------------------------
# DELETE /v1/restaurants?restaurant_id={id}
# ---------------------------------------------------------------------------

async def test_delete_restaurant_success(client, mock_restaurant_service):
    mock_restaurant_service.delete.reset_mock()
    mock_restaurant_service.delete.return_value = None

    response = await client.delete(BASE, params={"restaurant_id": 1})

    assert response.status_code == 200
    mock_restaurant_service.delete.assert_awaited_once_with(
        restaurant_id=1, user_id=1
    )


async def test_delete_restaurant_not_found(client, mock_restaurant_service):
    mock_restaurant_service.delete.reset_mock()
    mock_restaurant_service.delete.side_effect = ResourceNotFoundException(
        "Restaurant not found"
    )

    response = await client.delete(BASE, params={"restaurant_id": 999})

    assert response.status_code == 404
    mock_restaurant_service.delete.side_effect = None