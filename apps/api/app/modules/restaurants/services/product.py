from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.exceptions import ResourceNotFoundException
from app.modules.restaurants.models import Product, Restaurant
from app.modules.restaurants.repositories.product import IProductRepository
from app.modules.restaurants.schemas.product import ProductRead, ProductCreate, ProductUpdate


class ProductService:

    def __init__(self, repo: IProductRepository, session: AsyncSession):
        self._repo = repo
        self._session = session

    async def _check_owner(self, restaurant_id: int, user_id: int):
        stmt = select(Restaurant).where(Restaurant.id == restaurant_id)
        result = await self._session.execute(stmt)
        restaurant = result.scalar_one_or_none()

        if not restaurant or restaurant.owner_id != user_id:
            raise ResourceNotFoundException("Restaurant not found")

    # 🔓 PUBLIC
    async def get_all_public(self, restaurant_id: int, limit: int = 10, offset: int = 0):
        products = await self._repo.get_all(restaurant_id, limit, offset)
        return [ProductRead.model_validate(p) for p in products]

    async def get_by_id_public(self, product_id: int, restaurant_id: int):
        product = await self._repo.get_by_id(product_id, restaurant_id)

        if not product:
            raise ResourceNotFoundException("Product not found")

        return ProductRead.model_validate(product)

    # 🔒 PRIVATE
    async def get_all_private(self, restaurant_id: int, user_id: int, limit: int = 10, offset: int = 0):
        await self._check_owner(restaurant_id, user_id)

        return await self.get_all_public(restaurant_id, limit, offset)

    async def get_by_id_private(self, product_id: int, restaurant_id: int, user_id: int):
        await self._check_owner(restaurant_id, user_id)

        return await self.get_by_id_public(product_id, restaurant_id)

    async def create(self, data: ProductCreate, restaurant_id: int, user_id: int):
        await self._check_owner(restaurant_id, user_id)

        product = Product(**data.model_dump(), restaurant_id=restaurant_id)

        product = await self._repo.create(product, restaurant_id)
        await self._session.commit()

        return ProductRead.model_validate(product)

    async def update(self, product_id: int, restaurant_id: int, user_id: int, data: ProductUpdate):
        await self._check_owner(restaurant_id, user_id)

        product = await self._repo.get_by_id(product_id, restaurant_id)
        if not product:
            raise ResourceNotFoundException("Product not found")

        payload = data.model_dump(exclude_unset=True)
        product = await self._repo.update(product, payload)

        await self._session.commit()
        return ProductRead.model_validate(product)

    async def delete(self, product_id: int, restaurant_id: int, user_id: int):
        await self._check_owner(restaurant_id, user_id)

        product = await self._repo.get_by_id(product_id, restaurant_id)
        if not product:
            raise ResourceNotFoundException("Product not found")

        await self._repo.delete(product)
        await self._session.commit()