from fastapi import APIRouter, Depends
from .service import PublicMenuService
from .schemas import PublicRestaurantProfile, PublicMenuRead, PublicCategoryRead
from .dependencies import get_restaurant_menu_service

router = APIRouter(prefix="/menu", tags=["Public Menu"])

@router.get("/{slug}", response_model=dict)
async def get_restaurant(slug: str, service: PublicMenuService = Depends(get_restaurant_menu_service)):
    restaurant, categories = await service.get_restaurant(slug)

    return {
        "profile": PublicRestaurantProfile.model_validate(restaurant),
        "menu": PublicMenuRead(
            name=restaurant.name,
            logo_url=restaurant.logo_url,
            categories=[
                PublicCategoryRead.model_validate(cat)
                for cat in categories
                if cat.products
            ],
        ),
    }