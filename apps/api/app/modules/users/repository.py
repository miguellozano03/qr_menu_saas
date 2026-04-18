from abc import ABC, abstractmethod
from datetime import datetime, UTC
from sqlalchemy import select, delete, update
from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.users.models import User
from app.modules.users.models import RefreshToken, TokenBlacklist

class IUserRepository(ABC):

    @abstractmethod
    async def get_user_by_id(self, user_id: int) -> User | None:
        pass

    @abstractmethod
    async def get_user_by_email(self, email: str)  -> User | None:
        pass

    @abstractmethod
    async def create(self, user: User) -> User:
        pass

    @abstractmethod
    async def update(self, user: User, data: dict) -> User:
        pass

    @abstractmethod
    async def delete(self, user: User) -> None:
        pass


class UserRepository(IUserRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_user_by_id(self, user_id: int) -> User | None:
        stmt = select(User).where(User.id == user_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
    
    async def get_user_by_email(self, email: str) -> User | None:
        stmt = select(User).where(User.email == email)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
    
    async def create(self, user: User) -> User:
        self.session.add(user)
        await self.session.flush()
        await self.session.refresh(user)
        return user
    
    async def update(self, user: User, data: dict) -> User:
        allowed_fields = {"email", "hashed_password"}
        
        for field, value in data.items():
            if field in allowed_fields:
                setattr(user, field, value)

        await self.session.flush()
        await self.session.refresh(user)
        return user
    
    async def delete(self, user: User) -> None:
        await self.session.delete(user)
        await self.session.flush()
        
class TokenRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    # --- Refresh tokens ---

    async def save_refresh_token(self, jti: str, user_id: int, expires_at: datetime) -> None:
        token = RefreshToken(jti=jti, user_id=user_id, expires_at=expires_at)
        self.session.add(token)
        await self.session.flush()

    async def get_refresh_token(self, jti: str) -> RefreshToken | None:
        stmt = select(RefreshToken).where(RefreshToken.jti == jti)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def revoke_refresh_token(self, jti: str) -> None:
        stmt = select(RefreshToken).where(RefreshToken.jti == jti)
        result = await self.session.execute(stmt)
        token = result.scalar_one_or_none()
        if token:
            token.revoked = True
            await self.session.flush()

    # --- Access token blacklist ---

    async def blacklist_access_token(self, jti: str, expires_at: datetime) -> None:
        entry = TokenBlacklist(jti=jti, expires_at=expires_at)
        self.session.add(entry)
        await self.session.flush()

    async def is_blacklisted(self, jti: str) -> bool:
        stmt = select(TokenBlacklist).where(TokenBlacklist.jti == jti)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none() is not None

    async def clean_expired_blacklist(self) -> None:
        stmt = delete(TokenBlacklist).where(TokenBlacklist.expires_at < datetime.now(UTC))
        await self.session.execute(stmt)