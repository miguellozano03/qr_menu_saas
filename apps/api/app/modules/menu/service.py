from sqlalchemy.ext.asyncio import AsyncSession
from app.core.exceptions import ResourceNotFoundException
from .repository import IPublicMenuRepository
from .schemas import PublicRestaurantProfile, PublicMenuRead, PublicCategoryRead

class PublicMenuService:
    def __init__(self, session: AsyncSession, repo: IPublicMenuRepository) -> None:
        self._session = session
        self._repo = repo
        
    async def get_restaurant_profile(self, slug: str) -> PublicRestaurantProfile:
        profile = await self._repo.get_restaurant_profile(slug)
        
        if profile is None:
            raise ResourceNotFoundException("Restaurant not found")
        
        return PublicRestaurantProfile.model_validate(profile)
        
    async def get_restaurant_menu(self, slug: str) -> PublicMenuRead:
        menu = await self._repo.get_restaurant_menu(slug)
        
        if menu is None:
            raise ResourceNotFoundException("Restaurant not found")
        
        return PublicMenuRead(
            name=menu.name,
            logo_url=menu.logo_url,
            categories=[
                PublicCategoryRead.model_validate(category)
                for category in sorted(
                    [c for c in menu.categories if c.products],
                    key=lambda c: (c.position is None, c.position)
                )
            ]
        )