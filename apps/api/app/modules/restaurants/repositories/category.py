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
            .where(Category.restaurant_id == restaurant_id)
            .where(Category.deleted_at.is_(None))
            .order_by(Category.position)
            .limit(limit)
            .offset(offset)
        )
        
        result = await self._session.execute(stmt)
        return result.scalars().all()
    
    async def get_by_id(self, category_id: int, restaurant_id: int) -> Category | None:
        stmt = (
            select(Category)
            .where(Category.id == category_id)
            .where(Category.restaurant_id == restaurant_id)
            .where(Category.deleted_at.is_(None))
        )
        result = await self._session.execute(stmt)
        
        return result.scalar_one_or_none()
    
    async def create(self, category: Category) -> Category:
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