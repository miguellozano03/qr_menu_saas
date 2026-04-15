from typing import Sequence
from abc import ABC, abstractmethod
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.restaurants.models import Product


class IProductRepository(ABC):

    @abstractmethod
    async def get_all(self, restaurant_id: int, limit: int = 10, offset: int = 0) -> Sequence[Product]:
        pass

    @abstractmethod
    async def get_by_id(self, product_id: int, restaurant_id: int) -> Product | None:
        pass

    @abstractmethod
    async def create(self, product: Product, restaurant_id: int) -> Product:
        pass

    @abstractmethod
    async def update(self, product: Product, data: dict) -> Product:
        pass

    @abstractmethod
    async def delete(self, product: Product) -> None:
        pass


class ProductRepository(IProductRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_all(self, restaurant_id: int, limit: int = 10, offset: int = 0) -> Sequence[Product]:
        stmt = (
            select(Product)
            .where(Product.restaurant_id == restaurant_id)
            .where(Product.deleted_at.is_(None))
            .order_by(Product.position)
            .limit(limit)
            .offset(offset)
        )
        result = await self._session.execute(stmt)
        return result.scalars().all()

    async def get_by_id(self, product_id: int, restaurant_id: int) -> Product | None:
        stmt = (
            select(Product)
            .where(Product.id == product_id)
            .where(Product.restaurant_id == restaurant_id)
            .where(Product.deleted_at.is_(None))
        )
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def create(self, product: Product, restaurant_id: int) -> Product:
        product.restaurant_id = restaurant_id

        self._session.add(product)
        await self._session.flush()
        await self._session.refresh(product)
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