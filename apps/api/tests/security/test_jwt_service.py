import pytest
from datetime import datetime, timedelta, UTC
from app.core.security.jwt_service import jwt_service, TokenPayload

@pytest.fixture(scope="module")
def service():
    return jwt_service

@pytest.fixture(scope="module")
def access_token(service):
    return service.create_access_token("user123")

@pytest.fixture(scope="module")
def expired_token(service):
    fixed_time = datetime(2000, 1, 1, tzinfo=UTC)
    return service._create_token(
    data=TokenPayload(
        sub="old_user",
        type="access",
        iat=fixed_time,
        exp=fixed_time,
    ),
    expires_delta=timedelta(seconds=-1),
    )

def test_create_and_decode_access_token(service, access_token):
    payload = service.decode_token(access_token)

    assert payload.sub == "user123"
    assert payload.type == "access"
    assert isinstance(payload.exp, datetime)

def test_verify_access_token_success(service, access_token):
    result = service.verify_access_token(access_token)

    assert result.sub == "user123"
    assert result.type == "access"

def test_verify_access_token_fails_with_refresh_token(service):
    refresh_token = service.create_refresh_token("test_user")
    
    with pytest.raises(ValueError, match="An access Token was expected"):
        service.verify_access_token(refresh_token)

def test_decode_expired_token(service, expired_token):
    with pytest.raises(ValueError, match="Token expired"):
        service.decode_token(expired_token)

def test_decode_invalid_token(service):
    with pytest.raises(ValueError, match="Token is invalid"):
        service.decode_token("isn't a token")
