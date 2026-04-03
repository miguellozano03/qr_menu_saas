from datetime import datetime, timedelta, UTC
from pydantic import BaseModel
import jwt
from app.core.config import settings

class TokenData(BaseModel):
    sub: str
    type: str

class TokenPayload(BaseModel):
    sub: str
    type: str
    iat: datetime
    exp: datetime

class JWTService:
    def __init__(self) -> None:
        self.secret_key = settings.secret_key
        self.algorithm = settings.algorithm
        self.access_token_expire_minutes = settings.access_token_expire_minutes
        self.refresh_token_expire_days = settings.refresh_token_expire_days

    def _create_token(self, data: TokenData, expires_delta: timedelta) -> str:
        now = datetime.now(UTC)
        payload = {
            "sub": data.sub,
            "type": data.type,
            "iat": now,
            "exp": now + expires_delta
        }

        return jwt.encode(payload, self.algorithm)
    
    def create_access_token(self, sub: str) -> str:
        data = TokenData(sub=sub, type="access")
        return self._create_token(data, timedelta(minutes=self.access_token_expire_minutes))

    def create_refresh_token(self, sub: str) -> str:
        data = TokenData(sub=sub, type="refresh")
        return self._create_token(data, timedelta(days=settings.refresh_token_expire_days))

    def decode_token(self, token: str):
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return TokenPayload(**payload)
        except jwt.ExpiredSignatureError:
            raise ValueError("Token expired")
        except jwt.InvalidTokenError:
            raise ValueError("Token is invalid")
        
    def verify_access_token(self, token: str):
        token_data = self.decode_token(token)
        if token_data.type != "access":
            raise ValueError("An access Token was expected")
        return token_data.model_dump()
    
    def verify_refresh_token(self, token: str):
        token_data = self.decode_token(token)
        if token_data.type != "refresh":
            raise ValueError("An refresh Token was expected")
        return token_data.model_dump()
    

jwt_service = JWTService()