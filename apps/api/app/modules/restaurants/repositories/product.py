from typing import Sequence
from abc import ABC, abstractmethod
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.restaurants.models import Product, Restaurant
from app.core.exceptions import ResourceNotFoundException


class IProductRepository(ABC):

    @abstractmethod
    async def get_all(self, restaurant_id: int, limit: int = 10, offset: int = 0) -> Sequence[Product]:
        """
        Retrieves all products for a specific restaurant belonging to the user.

        Returns:
            List of product domain entities
        """
        pass

    @abstractmethod
    async def get_by_id(self, product_id: int, restaurant_id: int) -> Product | None:
        """Retrieves a product by its ID, ensuring it belongs to the user's restaurant."""
        pass

    @abstractmethod
    async def create(self, product: Product, restaurant_id: int) -> Product:
        """
        Create a new product.
        """
        pass

    @abstractmethod
    async def update(self, product: Product, data: dict) -> Product:
        """
        Update a product information.

        Returns:
            Product model object
        """
        pass

    @abstractmethod
    async def delete(self, product: Product) -> None:
        """
        Delete a product (soft delete)
        """
        pass


class ProductRepository(IProductRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_all(self, restaurant_id: int, limit: int = 10, offset: int = 0) -> Sequence[Product]:
        stmt = (
            select(Product)
            .join(Restaurant, Product.restaurant_id == Restaurant.id)
            .where(Product.restaurant_id == restaurant_id)
            .order_by(Product.position)
            .limit(limit)
            .offset(offset)
        )
        result = await self._session.execute(stmt)
        return result.scalars().all()

    async def get_by_id(self, product_id: int, restaurant_id: int) -> Product | None:
        stmt = (
            select(Product)
            .join(Restaurant, Product.restaurant_id == Restaurant.id)
            .where(Product.id == product_id)
            .where(Product.restaurant_id == restaurant_id)
        )
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def create(self, product: Product, restaurant_id: int) -> Product:
        stmt = (
            select(Restaurant)
            .where(Restaurant.id == restaurant_id)
        )

        result = await self._session.execute(stmt)
        restaurant = result.scalar_one_or_none()

        if not restaurant:
            raise ResourceNotFoundException("Restaurant not found or not allowed")

        product.restaurant_id = restaurant_id

        self._session.add(product)
        await self._session.flush()
        await self._session.refresh(product)
        await self._session.commit()
        return product

    async def update(self, product: Product, data: dict) -> Product:
        for key, value in data.items():
            setattr(product, key, value)

        await self._session.flush()
        await self._session.refresh(product)
        return product

    async def delete(self, product: Product) -> None:
        product.soft_delete()
        await self._session.flush()