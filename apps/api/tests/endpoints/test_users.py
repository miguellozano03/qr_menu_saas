import pytest
from datetime import datetime, timezone
from unittest.mock import AsyncMock, MagicMock
from httpx import AsyncClient, ASGITransport

from app.main import app
from app.modules.users.router import get_auth_service, get_user_service, get_current_user
from app.modules.users.schemas import UserRead, TokenResponse, RegisterResponse
from app.core.exceptions import UnauthorizedException, ResourceNotFoundException, IsDuplicatedException


AUTH  = "/v1/auth"
USERS = "/v1/users"

# ---------------------------------------------------------------------------
# Test Data
# ---------------------------------------------------------------------------

FAKE_USER = UserRead(id=1, email="test@example.com", created_at=datetime(2024, 1, 1, tzinfo=timezone.utc))

FAKE_TOKEN_RESPONSE = TokenResponse(
    access_token="access.jwt.token",
    refresh_token="refresh.jwt.token",
    token_type="bearer",
)

FAKE_REGISTER_RESPONSE = RegisterResponse(
    user=FAKE_USER,
    access_token="access.jwt.token",
    refresh_token="refresh.jwt.token",
)

VALID_REGISTER = {"email": "test@example.com", "password": "Secret123"}
VALID_LOGIN    = {"email": "test@example.com", "password": "Secret123"}


# ---------------------------------------------------------------------------
# Local Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture()
def mock_auth_service():
    service = MagicMock()
    service.register = AsyncMock()
    service.login    = AsyncMock()
    return service


@pytest.fixture()
def mock_user_service():
    service = MagicMock()
    service.get_user_by_id = AsyncMock()
    service.update_user    = AsyncMock()
    service.delete_account = AsyncMock()
    return service


@pytest.fixture()
async def client(mock_auth_service, mock_user_service):
    """
    Cliente con tres overrides:
      - get_auth_service  → mock_auth_service
      - get_user_service  → mock_user_service
      - get_current_user  → FAKE_USER (evita validar JWT en rutas protegidas)
    """
    app.dependency_overrides[get_auth_service]  = lambda: mock_auth_service
    app.dependency_overrides[get_user_service]  = lambda: mock_user_service
    app.dependency_overrides[get_current_user]  = lambda: FAKE_USER

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac

    app.dependency_overrides.clear()


# ---------------------------------------------------------------------------
# POST /v1/auth/register
# ---------------------------------------------------------------------------

async def test_register_success(client, mock_auth_service):
    mock_auth_service.register.return_value = FAKE_REGISTER_RESPONSE

    response = await client.post(f"{AUTH}/register", json=VALID_REGISTER)

    assert response.status_code == 200
    body = response.json()
    assert body["user"]["email"] == "test@example.com"
    assert "access_token" in body
    mock_auth_service.register.assert_awaited_once()


async def test_register_duplicate_email(client, mock_auth_service):
    mock_auth_service.register.side_effect = IsDuplicatedException("Email already registered")

    response = await client.post(f"{AUTH}/register", json=VALID_REGISTER)

    assert response.status_code == 409
    mock_auth_service.register.side_effect = None


async def test_register_invalid_body_missing_password(client, mock_auth_service):
    response = await client.post(f"{AUTH}/register", json={"email": "test@example.com"})

    assert response.status_code == 422
    mock_auth_service.register.assert_not_awaited()


async def test_register_invalid_body_weak_password(client, mock_auth_service):
    """Validador de Pydantic rechaza passwords sin mayúscula/número."""
    response = await client.post(f"{AUTH}/register", json={"email": "test@example.com", "password": "weakpassword"})

    assert response.status_code == 422
    mock_auth_service.register.assert_not_awaited()


async def test_register_invalid_email(client, mock_auth_service):
    response = await client.post(f"{AUTH}/register", json={"email": "not-an-email", "password": "Secret123"})

    assert response.status_code == 422
    mock_auth_service.register.assert_not_awaited()


# ---------------------------------------------------------------------------
# POST /v1/auth/login
# ---------------------------------------------------------------------------

async def test_login_success(client, mock_auth_service):
    mock_auth_service.login.return_value = FAKE_TOKEN_RESPONSE

    response = await client.post(f"{AUTH}/login", json=VALID_LOGIN)

    assert response.status_code == 200
    body = response.json()
    assert body["token_type"] == "bearer"
    assert "access_token" in body
    mock_auth_service.login.assert_awaited_once()


async def test_login_wrong_credentials(client, mock_auth_service):
    mock_auth_service.login.side_effect = UnauthorizedException("Email or password incorrect")

    response = await client.post(f"{AUTH}/login", json=VALID_LOGIN)

    assert response.status_code == 401
    mock_auth_service.login.side_effect = None


async def test_login_invalid_body(client, mock_auth_service):
    response = await client.post(f"{AUTH}/login", json={"email": "bad"})

    assert response.status_code == 422
    mock_auth_service.login.assert_not_awaited()


# ---------------------------------------------------------------------------
# GET /v1/users/me
# ---------------------------------------------------------------------------

async def test_get_me_success(client):
    response = await client.get(f"{USERS}/me")

    assert response.status_code == 200
    body = response.json()
    assert body["id"] == 1
    assert body["email"] == "test@example.com"


# ---------------------------------------------------------------------------
# PATCH /v1/users/me
# ---------------------------------------------------------------------------

async def test_update_me_success(client, mock_user_service):
    mock_user_service.update_user.return_value = None

    response = await client.patch(f"{USERS}/me", json={"email": "new@example.com"})

    assert response.status_code == 200
    mock_user_service.update_user.assert_awaited_once_with(
        FAKE_USER.id, mock_user_service.update_user.call_args.args[1]
    )


async def test_update_me_invalid_email(client, mock_user_service):
    response = await client.patch(f"{USERS}/me", json={"email": "not-valid"})

    assert response.status_code == 422
    mock_user_service.update_user.assert_not_awaited()


async def test_update_me_weak_password(client, mock_user_service):
    response = await client.patch(f"{USERS}/me", json={"password": "nouppercase1"})

    assert response.status_code == 422
    mock_user_service.update_user.assert_not_awaited()


# ---------------------------------------------------------------------------
# DELETE /v1/users/delete_account
# ---------------------------------------------------------------------------

async def test_delete_account_success(client, mock_user_service):
    mock_user_service.delete_account.return_value = None

    response = await client.delete(f"{USERS}/delete_account")

    assert response.status_code == 200
    mock_user_service.delete_account.assert_awaited_once_with(FAKE_USER.id)


async def test_delete_account_not_found(client, mock_user_service):
    mock_user_service.delete_account.side_effect = ResourceNotFoundException("User not found")

    response = await client.delete(f"{USERS}/delete_account")

    assert response.status_code == 404
    mock_user_service.delete_account.side_effect = None