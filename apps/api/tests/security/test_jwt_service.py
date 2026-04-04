import pytest
from datetime import datetime, timedelta, UTC
from app.core.security.jwt_service import jwt_service, TokenPayload

@pytest.fixture
def service():
    return jwt_service

def test_create_and_decode_access_token(service):
    user_id = "user123"

    token = service.create_access_token(user_id)
    payload = service.decode_token(token)

    assert payload.sub == user_id
    assert payload.type == "access"
    assert isinstance(payload.exp, datetime)

def test_verify_access_token_sucess(service):
    token = service.create_access_token("user123")
    result = service.verify_access_token(token)

    assert result.get("sub") == "user123"
    assert result.get("type") == "access"

def test_verify_access_token_fails_with_refresh_token(service):
    refresh_token = service.create_refresh_token("test_user")
    
    with pytest.raises(ValueError, match="An access Token was expected"):
        service.verify_access_token(refresh_token)

def test_decode_expired_token(service, monkeypatch):
    user_id = "old_user"
    token = service._create_token(
        data=TokenPayload(sub=user_id, type="access", iat=datetime.now(UTC), exp=datetime.now(UTC)),
        expires_delta=timedelta(seconds=-1)
    )
    
    with pytest.raises(ValueError, match="Token expired"):
        service.decode_token(token)

def test_decode_invalid_token(service):
    with pytest.raises(ValueError, match="Token is invalid"):
        service.decode_token("isn't a token")
