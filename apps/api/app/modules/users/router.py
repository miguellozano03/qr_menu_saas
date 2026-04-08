from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db.database import get_db
from app.core.security.password_service import password_service
from app.core.security.jwt_service import jwt_service
from app.core.exceptions import UnauthorizedException, ResourceNotFoundException
from app.modules.users.schemas import TokenResponse, LoginData, RegisterResponse, UserCreate, UserRead, UserUpdate
from app.modules.users.services.auth_service import AuthService
from app.modules.users.services.user_service import UserService
from app.modules.users.repository import UserRepository

auth_router = APIRouter(prefix="/auth", tags=["Authentication"])
user_router = APIRouter(prefix="/users", tags=["Users"])


# ==========================================
# HELPERS
# ==========================================

bearer_scheme = HTTPBearer()

async def get_auth_service(session: AsyncSession = Depends(get_db)) -> AuthService:
    return AuthService(
        repo=UserRepository(session),
        session=session,
        password_service=password_service,
        jwt_service=jwt_service
    )

async def get_user_service(session: AsyncSession = Depends(get_db)) -> UserService:
    return UserService(
        repo=UserRepository(session),
        session=session
    )

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    service: UserService = Depends(get_user_service)
) -> UserRead:
    
    try:
        payload = jwt_service.verify_access_token(credentials.credentials) 
    except ValueError as e:
        raise UnauthorizedException(str(e))
    
    user = await service.get_user_by_id(int(payload.sub))
    if not user:
        raise ResourceNotFoundException("User not found for the provided token")
    return user
    
# ==========================================
# AUTHENTICATION ROUTES
# ==========================================

@auth_router.post(
    "/register",
    response_model=RegisterResponse,
    summary="Create a new account",
    description="Creates a new user account in the system.",
    responses={
        409: {"description": "Email already registered"}
    }
)
async def register(data: UserCreate, service: AuthService = Depends(get_auth_service)):
    return await service.register(data)

@auth_router.post(
    "/login", response_model=TokenResponse,
    summary="Login an account",
    description="Login an account within the system",
    responses={
        401: {"description": "Email or password incorrect"}
    }
)
async def login(data: LoginData, service: AuthService = Depends(get_auth_service)):
    return await service.login(data)


# ==========================================
# USERS ROUTES
# ==========================================

@user_router.get(
    "/me",
    response_model= UserRead,
    summary="Get current authenticated user",
    description="Returns information of the currently authenticated user based on the provider JWT access Token",
    responses={
        401: {"description": "Not authenticated or invalid token"},
        404: {"description": "User not found"},
    },
)
async def me(current_user: UserRead = Depends(get_current_user)):
    return current_user


@user_router.patch(
    "/me",
    summary="Update an account details (user) of the platform",
    description="Update the information of an authenticated user",
)
async def update_account(data: UserUpdate, current_user: UserRead = Depends(get_current_user), service: UserService = Depends(get_user_service)):
    await service.update_user(current_user.id, data)

@user_router.delete(
    "/delete_account",
    summary="Delete an account(user) of the platform.",
    description="Delete an authenticated user from the system.",
    responses={
        401: {"description": "Not authenticated"},
        401: {"description": "Not authenticated"},
        404: {"description": "User not found"},
    }
)
async def delete_account(current_user: UserRead = Depends(get_current_user), service: UserService = Depends(get_user_service)):
    await service.delete_account(current_user.id)