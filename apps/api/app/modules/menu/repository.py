from abc import ABC, abstractmethod
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.modules.restaurants.models import Restaurant, Category, Product


class IPublicMenuRepository(ABC):
    @abstractmethod
    async def get_restaurant_profile(self, slug: str) -> Restaurant | None:
        pass
    
    @abstractmethod
    async def get_restaurant_menu(self, slug: str) -> Restaurant | None:
        pass


class PublicMenuRepository(IPublicMenuRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session
        
    async def get_restaurant_profile(self, slug: str) -> Restaurant | None:
        stmt = (
            select(Restaurant)
            .where(Restaurant.slug == slug, Restaurant.deleted_at.is_(None))
            .options(selectinload(Restaurant.links))
        )
        
        result = await self._session.execute(stmt)
        
        return result.scalar_one_or_none()
    
    async def get_restaurant_menu(self, slug: str) -> Restaurant | None:
        stmt = (
            select(Restaurant)
            .where(Restaurant.slug == slug, Restaurant.deleted_at.is_(None))
            .options(selectinload(Restaurant.categories).selectinload(Category.products))
        )
        
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()
        