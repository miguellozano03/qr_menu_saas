from typing import Sequence
from abc import ABC, abstractmethod
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.restaurants.models import Restaurant


class IRestaurantRepository(ABC):

    @abstractmethod
    async def get_all(self, user_id: int, limit: int = 10, offset: int = 0) -> Sequence[Restaurant]:
        """
        Retrieves all restaurants belonging to the account user.

        Returns:
            List of all restaurant domain entities
        """
        pass

    @abstractmethod
    async def get_by_id(self, restaurant_id: int, user_id: int) -> Restaurant | None:
        """Retrieves a restaurant by its ID."""
        pass

    @abstractmethod
    async def get_by_slug(self, slug: str, user_id: int) -> Restaurant | None:
        """Retrieves a restaurant by its slug"""
        pass

    @abstractmethod
    async def create(self, restaurant: Restaurant) -> Restaurant:
        """
        Create a new restaurant for the account owner.
        """
        pass

    @abstractmethod
    async def update(self, restaurant: Restaurant, data: dict) -> Restaurant:
        """
        Update an restaurant information.

        Args:
            restaurant_id (int): ID of restaurant.

        Returns:
            Restaurant model object
        """
        pass

    @abstractmethod
    async def delete(self, restaurant: Restaurant) -> None:
        """
        Delete a restaurant (soft delete)

        Args:
            restaurant_id (int): ID of restaurant.
        """
        pass

class RestaurantRepository(IRestaurantRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session  = session

    async def get_all(self, user_id: int, limit: int = 10, offset: int = 0) -> Sequence[Restaurant]:
        stmt = (
            select(Restaurant)
            .where(Restaurant.owner_id == user_id)
            .order_by(Restaurant.created_at.desc())
            .limit(limit)
            .offset(offset)
        )
        result = await self._session.execute(stmt)
        return result.scalars().all()
    
    async def get_by_id(self, restaurant_id: int, user_id: int) -> Restaurant | None:
        stmt = select(Restaurant).where(Restaurant.owner_id == user_id).where(Restaurant.id == restaurant_id)
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()
    
    async def get_by_slug(self, slug: str, user_id: int) -> Restaurant | None:
        stmt = select(Restaurant).where(Restaurant.owner_id == user_id).where(Restaurant.slug == slug)
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()
    
    async def create(self, restaurant: Restaurant) -> Restaurant:
        self._session.add(restaurant)
        await self._session.flush()
        await self._session.refresh(restaurant)
        await self._session.commit()
        return restaurant
    
    async def update(self, restaurant: Restaurant, data: dict) -> Restaurant:
        for key, value in data.items():
            setattr(restaurant, key, value)

        await self._session.flush()
        await self._session.refresh(restaurant)
        return restaurant

    async def delete(self, restaurant: Restaurant) -> None:
        restaurant.soft_delete()
        await self._session.flush()