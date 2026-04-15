from typing import Sequence
from abc import ABC, abstractmethod
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.restaurants.models import RestaurantLink


class IRestaurantLinkRepository(ABC):

    @abstractmethod
    async def get_all(self, restaurant_id: int, limit: int = 10, offset: int = 0) -> Sequence[RestaurantLink]:
        pass

    @abstractmethod
    async def get_by_id(self, link_id: int, restaurant_id: int) -> RestaurantLink | None:
        pass

    @abstractmethod
    async def create(self, link: RestaurantLink, restaurant_id: int) -> RestaurantLink:
        pass

    @abstractmethod
    async def update(self, link: RestaurantLink, data: dict) -> RestaurantLink:
        pass

    @abstractmethod
    async def delete(self, link: RestaurantLink) -> None:
        pass


class RestaurantLinkRepository(IRestaurantLinkRepository):

    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_all(self, restaurant_id: int, limit: int = 10, offset: int = 0):
        stmt = (
            select(RestaurantLink)
            .where(RestaurantLink.restaurant_id == restaurant_id)
            .where(RestaurantLink.deleted_at.is_(None))
            .order_by(RestaurantLink.position)
            .limit(limit)
            .offset(offset)
        )
        result = await self._session.execute(stmt)
        return result.scalars().all()

    async def get_by_id(self, link_id: int, restaurant_id: int):
        stmt = (
            select(RestaurantLink)
            .where(RestaurantLink.id == link_id)
            .where(RestaurantLink.restaurant_id == restaurant_id)
            .where(RestaurantLink.deleted_at.is_(None))
        )
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def create(self, link: RestaurantLink, restaurant_id: int):
        link.restaurant_id = restaurant_id

        self._session.add(link)
        await self._session.flush()
        await self._session.refresh(link)
        return link

    async def update(self, link: RestaurantLink, data: dict):
        for k, v in data.items():
            setattr(link, k, v)

        await self._session.flush()
        await self._session.refresh(link)
        return link

    async def delete(self, link: RestaurantLink):
        link.soft_delete()
        await self._session.flush()