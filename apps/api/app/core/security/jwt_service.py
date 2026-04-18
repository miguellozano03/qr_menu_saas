from abc import ABC, abstractmethod
from datetime import datetime, timedelta, UTC
from pydantic import BaseModel
import jwt
import uuid
from app.core.config import settings

class TokenData(BaseModel):
    sub: str
    type: str

class TokenPayload(BaseModel):
    sub: str
    type: str
    jti: str
    iat: datetime
    exp: datetime

class IJWTService(ABC):
    @abstractmethod
    def create_access_token(self, sub: str) -> tuple[str, str]: pass
    @abstractmethod
    def create_refresh_token(self, sub: str) -> tuple[str, str]: pass
    @abstractmethod
    def decode_token(self, token: str) -> TokenPayload: pass
    @abstractmethod
    def verify_access_token(self, token: str) -> TokenPayload: pass
    @abstractmethod
    def verify_refresh_token(self, token: str) -> TokenPayload: pass

class JWTService(IJWTService):
    def __init__(self) -> None:
        self.secret_key = settings.secret_key
        self.algorithm = settings.algorithm
        self.access_token_expire_minutes = settings.access_token_expire_minutes
        self.refresh_token_expire_days = settings.refresh_token_expire_days

    def _create_token(self, data: TokenData, expires_delta: timedelta) -> tuple[str, str]:
        now = datetime.now(UTC)
        jti = str(uuid.uuid4())
        payload = {
            "sub": data.sub,
            "type": data.type,
            "jti": jti,
            "iat": int(now.timestamp()),
            "exp": int((now + expires_delta).timestamp())
        }
        token = jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
        return token, jti

    def create_access_token(self, sub: str) -> tuple[str, str]:
        data = TokenData(sub=sub, type="access")
        return self._create_token(data, timedelta(minutes=self.access_token_expire_minutes))

    def create_refresh_token(self, sub: str) -> tuple[str, str]:
        data = TokenData(sub=sub, type="refresh")
        return self._create_token(data, timedelta(days=self.refresh_token_expire_days))

    def decode_token(self, token: str) -> TokenPayload:
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return TokenPayload(**payload)
        except jwt.ExpiredSignatureError:
            raise ValueError("Token expired")
        except jwt.InvalidTokenError:
            raise ValueError("Token is invalid")

    def verify_access_token(self, token: str) -> TokenPayload:
        token_data = self.decode_token(token)
        if token_data.type != "access":
            raise ValueError("An access token was expected")
        return token_data

    def verify_refresh_token(self, token: str) -> TokenPayload:
        token_data = self.decode_token(token)
        if token_data.type != "refresh":
            raise ValueError("A refresh token was expected")
        return token_data

jwt_service = JWTService()