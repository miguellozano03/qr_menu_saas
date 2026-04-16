from fastapi import APIRouter, Depends
from .service import PublicMenuService
from .schemas import PublicRestaurantProfile, PublicMenuRead
from .dependencies import get_restaurant_menu_service

router = APIRouter(prefix="/menu", tags=["Public Menu"])

@router.get("/{slug}/profile", response_model=PublicRestaurantProfile)
async def get_restaurant_profile(slug: str, service: PublicMenuService = Depends(get_restaurant_menu_service)):
    return await service.get_restaurant_profile(slug)

@router.get("/{slug}/", response_model=PublicMenuRead)
async def get_restaurant_menu(slug: str, service: PublicMenuService = Depends(get_restaurant_menu_service)):
    return await service.get_restaurant_menu(slug)