from fastapi import APIRouter
from app.modules.users.router import auth_router, user_router
from app.modules.restaurants.router import restaurants
from app.modules.menu.router import router as menu

api_router = APIRouter(prefix="/v1")

api_router.include_router(auth_router)
api_router.include_router(user_router)
api_router.include_router(restaurants)
api_router.include_router(menu)