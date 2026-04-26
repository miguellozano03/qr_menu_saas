from sqlalchemy.ext.asyncio import AsyncSession
from app.core.exceptions import ResourceNotFoundException
from .repository import IPublicMenuRepository
from .schemas import PublicRestaurantProfile, PublicMenuRead, PublicCategoryRead

class PublicMenuService:
    def __init__(self, session: AsyncSession, repo: IPublicMenuRepository) -> None:
        self._session = session
        self._repo = repo

    async def get_restaurant(self, slug: str):
        restaurant = await self._repo.get_restaurant(slug)

        if restaurant is None:
            raise ResourceNotFoundException("Restaurant not found")
        
        categories = sorted(
            restaurant.categories,
            key=lambda c: (c.position is None, c.position),
        )

        return restaurant, categories