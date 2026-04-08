from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security.password_service import IPasswordService
from app.core.security.jwt_service import JWTService
from app.core.exceptions import IsDuplicatedException, UnauthorizedException
from app.modules.users.repository import UserRepository
from app.modules.users.schemas import UserCreate, RegisterResponse, UserRead, LoginData, TokenResponse
from app.modules.users.models import User


class AuthService:
    def __init__(
        self,
        repo: UserRepository,
        session: AsyncSession,
        password_service: IPasswordService,
        jwt_service: JWTService
    ) -> None:
        self._repo = repo
        self._session = session
        self._password = password_service
        self._jwt = jwt_service

    async def register(self, data: UserCreate) -> RegisterResponse:
        exists = await self._repo.get_user_by_email(data.email)
        if exists:
            raise IsDuplicatedException("Email already registered")
        
        user = User(
            email=data.email,
            hashed_password=self._password.hash(data.password)
        )

        user = await self._repo.create(user)
        await self._session.commit()

        return RegisterResponse(
            user=UserRead.model_validate(user),
            access_token=self._jwt.create_access_token(str(user.id)),
            refresh_token=self._jwt.create_refresh_token(str(user.id))
        )
    
    async def login(self, data: LoginData) -> TokenResponse:
        user = await self._repo.get_user_by_email(data.email)
        if not user or not self._password.verify(data.password, user.hashed_password):
            raise UnauthorizedException("Email or password incorrect")
        
        return TokenResponse(
            access_token=self._jwt.create_access_token(str(user.id)),
            refresh_token=self._jwt.create_refresh_token(str(user.id))
        )