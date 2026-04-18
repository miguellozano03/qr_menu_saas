from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.exceptions import ResourceNotFoundException
from app.modules.restaurants.models import Product, Restaurant
from app.modules.restaurants.repositories.product import IProductRepository
from app.modules.restaurants.schemas.product import ProductRead, ProductCreate, ProductUpdate
from app.shared.storage.base import StorageService


class ProductService:

    def __init__(self, repo: IProductRepository, session: AsyncSession, storage: StorageService):
        self._repo = repo
        self._session = session
        self._storage = storage

    async def _check_owner(self, restaurant_id: int, user_id: int):
        stmt = select(Restaurant).where(Restaurant.id == restaurant_id)
        result = await self._session.execute(stmt)
        restaurant = result.scalar_one_or_none()

        if restaurant is None or restaurant.owner_id != user_id:
            raise ResourceNotFoundException("Restaurant not found")

    async def get_all(self, restaurant_id: int, user_id: int, limit: int = 10, offset: int = 0):
        await self._check_owner(restaurant_id, user_id)

        products = await self._repo.get_all(restaurant_id, limit, offset)
        return [ProductRead.model_validate(p) for p in products]

    async def get_by_id(self, product_id: int, restaurant_id: int, user_id: int):
        await self._check_owner(restaurant_id, user_id)

        product = await self._repo.get_by_id(product_id, restaurant_id)

        if product is None:
            raise ResourceNotFoundException("Product not found")

        return ProductRead.model_validate(product)

    async def create(self, data: ProductCreate, restaurant_id: int, user_id: int, product_img: UploadFile | None = None):
        await self._check_owner(restaurant_id, user_id)
        
        image_url = None
        if product_img is not None:
            image_url = await self._storage.upload(product_img)

        product = Product(
            category_id=data.category_id,
            name=data.name,
            description=data.description,
            price=data.price,
            image_url=image_url,
            is_available=data.is_available,
            position=data.position,
        )

        created = await self._repo.create(product, restaurant_id)
        await self._session.commit()

        return ProductRead.model_validate(created)

    async def update(self, data: ProductUpdate,  product_id: int, restaurant_id: int, user_id: int, product_img: UploadFile | None = None):
        await self._check_owner(restaurant_id, user_id)

        product = await self._repo.get_by_id(product_id, restaurant_id)

        if product is None:
            raise ResourceNotFoundException("Product not found")
        
        if product_img is not None:
            image_url = await self._storage.upload(product_img)
            product.image_url = image_url

        updated = await self._repo.update(product, data.model_dump(exclude_unset=True))
        await self._session.commit()

        return ProductRead.model_validate(updated)

    async def delete(self, product_id: int, restaurant_id: int, user_id: int):
        await self._check_owner(restaurant_id, user_id)

        product = await self._repo.get_by_id(product_id, restaurant_id)

        if product is None:
            raise ResourceNotFoundException("Product not found")

        await self._repo.delete(product)
        await self._session.commit()