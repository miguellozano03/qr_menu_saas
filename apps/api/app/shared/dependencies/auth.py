from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db.database import get_db
from app.core.security.jwt_service import jwt_service
from app.core.exceptions import UnauthorizedException
from app.modules.users.repository import TokenRepository

bearer_scheme = HTTPBearer()

async def get_current_user_id(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    session: AsyncSession = Depends(get_db),
) -> int:
    try:
        payload = jwt_service.verify_access_token(credentials.credentials)
    except ValueError:
        raise UnauthorizedException("Invalid or expired token")

    token_repo = TokenRepository(session)
    if await token_repo.is_blacklisted(payload.jti):
        raise UnauthorizedException("Token has been revoked")

    return int(payload.sub)