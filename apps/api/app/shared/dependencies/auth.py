from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.core.security.jwt_service import jwt_service
from app.core.exceptions import UnauthorizedException

bearer_scheme = HTTPBearer()


async def get_current_user_id(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> int:
    try:
        payload = jwt_service.verify_access_token(credentials.credentials)
        return int(payload.sub)
    except ValueError:
        raise UnauthorizedException("Invalid or expired token")