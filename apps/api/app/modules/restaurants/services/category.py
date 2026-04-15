from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.exceptions import ResourceNotFoundException
from app.modules.restaurants.models import Category, Restaurant
from app.modules.restaurants.repositories.category import ICategoryRepository
from app.modules.restaurants.schemas.category import (
    CategoryRead,
    CategoryCreate,
    CategoryUpdate,
)


class CategoryService:

    def __init__(self, repo: ICategoryRepository, session: AsyncSession):
        self._repo = repo
        self._session = session

    async def _check_owner(self, restaurant_id: int, user_id: int):
        stmt = select(Restaurant).where(Restaurant.id == restaurant_id)
        result = await self._session.execute(stmt)
        restaurant = result.scalar_one_or_none()

        if restaurant is None or restaurant.owner_id != user_id:
            raise ResourceNotFoundException("Restaurant not found")

    async def get_all(self, restaurant_id: int, user_id: int, limit: int = 10, offset: int = 0):
        await self._check_owner(restaurant_id, user_id)

        categories = await self._repo.get_all(restaurant_id, limit, offset)
        return [CategoryRead.model_validate(c) for c in categories]

    async def get_by_id(self, category_id: int, restaurant_id: int, user_id: int):
        await self._check_owner(restaurant_id, user_id)

        category = await self._repo.get_by_id(category_id, restaurant_id)

        if category is None:
            raise ResourceNotFoundException("Category not found")

        return CategoryRead.model_validate(category)

    async def create(self, data: CategoryCreate, restaurant_id: int, user_id: int):
        await self._check_owner(restaurant_id, user_id)

        category = Category(**data.model_dump(), restaurant_id=restaurant_id)

        created = await self._repo.create(category)
        await self._session.commit()

        return CategoryRead.model_validate(created)

    async def update(self, category_id: int, restaurant_id: int, user_id: int, data: CategoryUpdate):
        await self._check_owner(restaurant_id, user_id)

        category = await self._repo.get_by_id(category_id, restaurant_id)

        if category is None:
            raise ResourceNotFoundException("Category not found")

        updated = await self._repo.update(category, data.model_dump(exclude_unset=True))
        await self._session.commit()

        return CategoryRead.model_validate(updated)

    async def delete(self, category_id: int, restaurant_id: int, user_id: int):
        await self._check_owner(restaurant_id, user_id)

        category = await self._repo.get_by_id(category_id, restaurant_id)

        if category is None:
            raise ResourceNotFoundException("Category not found")

        await self._repo.delete(category)
        await self._session.commit()