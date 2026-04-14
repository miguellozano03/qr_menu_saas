from typing import Sequence
from abc import ABC, abstractmethod
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.restaurants.models import Category, Restaurant
from app.core.exceptions import ResourceNotFoundException

class ICategoryRepository(ABC):
    
    @abstractmethod
    async def get_all(self, restaurant_id: int, limit: int, offset: int) -> Sequence[Category]:
        pass
    
    @abstractmethod
    async def get_by_id(self, category_id: int, restaurant_id: int) -> Category | None:
        pass
    
    @abstractmethod
    async def create(self, category: Category) -> Category:
        pass
    
    @abstractmethod
    async def update(self, category: Category, data: dict) -> Category:
        pass
    
    @abstractmethod
    async def delete(self, category: Category) -> None:
        pass
    
class CategoryRepository(ICategoryRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session
    
    async def get_all(self, restaurant_id: int, limit: int, offset: int) -> Sequence[Category]:
        stmt = (
            select(Category)
            .join(Restaurant, Category.restaurant_id == Restaurant.id)
            .where(Restaurant.id == restaurant_id)
            .offset(offset)
            .order_by(Category.position)
            .limit(limit)
        )
        
        result = await self._session.execute(stmt)
        return result.scalars().all()
    
    async def get_by_id(self, category_id: int, restaurant_id: int) -> Category | None:
        stmt = (
            select(Category)
            .join(Restaurant, Category.restaurant_id == Restaurant.id)
            .where(Category.id == category_id)
            .where(Restaurant.id == restaurant_id)
        )
        result = await self._session.execute(stmt)
        
        return result.scalar_one_or_none()
    
    async def create(self, category: Category) -> Category:
        stmt = (
            select(Restaurant)
            .where(Restaurant.id == category.restaurant_id)
        )

        result = await self._session.execute(stmt)
        restaurant = result.scalar_one_or_none()

        if not restaurant:
            raise ResourceNotFoundException("Restaurant not found or not allowed")

        self._session.add(category)
        await self._session.flush()
        await self._session.refresh(category)
        return category
    
    async def update(self, category: Category, data: dict) -> Category:
        for key, value in data.items():
            setattr(category, key, value)
        
        await self._session.flush()
        await self._session.refresh(category)
        return category
    
    async def delete(self, category: Category) -> None:
        category.soft_delete()
        await self._session.flush()
