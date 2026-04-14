from fastapi import APIRouter

from .restaurant import router as restaurant_router
from .link import router as link_router
from .category import router as category_router
from .product import router as product_router

restaurants = APIRouter()

restaurants.include_router(restaurant_router)
restaurants.include_router(link_router)
restaurants.include_router(category_router)
restaurants.include_router(product_router)