from datetime import datetime, timedelta, UTC
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security.password_service import IPasswordService
from app.core.security.jwt_service import JWTService
from app.core.exceptions import IsDuplicatedException, UnauthorizedException
from app.modules.users.repository import UserRepository, TokenRepository
from app.modules.users.schemas import UserCreate, RegisterResponse, UserRead, LoginData, TokenResponse
from app.modules.users.models import User


class AuthService:
    def __init__(
        self,
        repo: UserRepository,
        token_repo: TokenRepository,
        session: AsyncSession,
        password_service: IPasswordService,
        jwt_service: JWTService,
    ) -> None:
        self._repo = repo
        self._token_repo = token_repo
        self._session = session
        self._password = password_service
        self._jwt = jwt_service

    def _refresh_token_expires_at(self) -> datetime:
        return datetime.now(UTC) + timedelta(days=self._jwt.refresh_token_expire_days)

    async def register(self, data: UserCreate) -> RegisterResponse:
        exists = await self._repo.get_user_by_email(data.email)
        if exists:
            raise IsDuplicatedException("Email already registered")

        user = User(
            email=data.email,
            hashed_password=self._password.hash(data.password),
        )
        user = await self._repo.create(user)

        access_token, _ = self._jwt.create_access_token(str(user.id))
        refresh_token, refresh_jti = self._jwt.create_refresh_token(str(user.id))

        await self._token_repo.save_refresh_token(
            jti=refresh_jti,
            user_id=user.id,
            expires_at=self._refresh_token_expires_at(),
        )
        await self._session.commit()

        return RegisterResponse(
            user=UserRead.model_validate(user),
            access_token=access_token,
            refresh_token=refresh_token,
        )

    async def login(self, data: LoginData) -> TokenResponse:
        user = await self._repo.get_user_by_email(data.email)
        if not user or not self._password.verify(data.password, user.hashed_password):
            raise UnauthorizedException("Email or password incorrect")

        access_token, _ = self._jwt.create_access_token(str(user.id))
        refresh_token, refresh_jti = self._jwt.create_refresh_token(str(user.id))

        await self._token_repo.save_refresh_token(
            jti=refresh_jti,
            user_id=user.id,
            expires_at=self._refresh_token_expires_at(),
        )
        await self._session.commit()

        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
        )

    async def refresh(self, refresh_token: str) -> TokenResponse:
        try:
            payload = self._jwt.verify_refresh_token(refresh_token)
        except ValueError as e:
            raise UnauthorizedException(str(e))

        db_token = await self._token_repo.get_refresh_token(payload.jti)
        if not db_token or db_token.revoked:
            raise UnauthorizedException("Refresh token revoked or not found")

        await self._token_repo.revoke_refresh_token(payload.jti)

        access_token, _ = self._jwt.create_access_token(payload.sub)
        new_refresh_token, new_refresh_jti = self._jwt.create_refresh_token(payload.sub)

        await self._token_repo.save_refresh_token(
            jti=new_refresh_jti,
            user_id=int(payload.sub),
            expires_at=self._refresh_token_expires_at(),
        )
        await self._session.commit()

        return TokenResponse(access_token=access_token, refresh_token=new_refresh_token)

    async def logout(self, access_token: str, refresh_token: str) -> None:
        try:
            refresh_payload = self._jwt.verify_refresh_token(refresh_token)
            await self._token_repo.revoke_refresh_token(refresh_payload.jti)
        except ValueError:
            pass  

        try:
            access_payload = self._jwt.verify_access_token(access_token)
            expires_at = datetime.fromtimestamp(access_payload.exp.timestamp(), tz=UTC)
            await self._token_repo.blacklist_access_token(
                jti=access_payload.jti,
                expires_at=expires_at,
            )
        except ValueError:
            pass

        await self._session.commit()