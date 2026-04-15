from typing import Sequence
from abc import ABC, abstractmethod
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.restaurants.models import Restaurant


class IRestaurantRepository(ABC):

    @abstractmethod
    async def get_all(self, limit: int = 10, offset: int = 0) -> Sequence[Restaurant]:
        pass

    @abstractmethod
    async def get_by_id(self, restaurant_id: int) -> Restaurant | None:
        pass

    @abstractmethod
    async def get_by_slug(self, slug: str) -> Restaurant | None:
        pass

    @abstractmethod
    async def create(self, restaurant: Restaurant) -> Restaurant:
        pass

    @abstractmethod
    async def update(self, restaurant: Restaurant, data: dict) -> Restaurant:
        pass

    @abstractmethod
    async def delete(self, restaurant: Restaurant) -> None:
        pass


class RestaurantRepository(IRestaurantRepository):

    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_all(self, limit: int = 10, offset: int = 0):
        stmt = (
            select(Restaurant)
            .order_by(Restaurant.created_at.desc())
            .where(Restaurant.deleted_at.is_(None))
            .limit(limit)
            .offset(offset)
        )
        result = await self._session.execute(stmt)
        return result.scalars().all()

    async def get_by_id(self, restaurant_id: int):
        stmt = (
            select(Restaurant)
            .where(Restaurant.id == restaurant_id)
            .where(Restaurant.deleted_at.is_(None))
        )
        
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_slug(self, slug: str):
        stmt =(
            select(Restaurant)
            .where(Restaurant.slug == slug)
            .where(Restaurant.deleted_at.is_(None))
        )
        
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def create(self, restaurant: Restaurant):
        self._session.add(restaurant)
        await self._session.flush()
        await self._session.refresh(restaurant)
        await self._session.commit()
        return restaurant

    async def update(self, restaurant: Restaurant, data: dict):
        for k, v in data.items():
            setattr(restaurant, k, v)

        await self._session.flush()
        await self._session.refresh(restaurant)
        return restaurant

    async def delete(self, restaurant: Restaurant):
        restaurant.soft_delete()
        await self._session.flush()