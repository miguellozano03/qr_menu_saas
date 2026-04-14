from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.exceptions import ResourceNotFoundException
from app.modules.restaurants.models import Category, Restaurant
from app.modules.restaurants.repositories.category import ICategoryRepository
from app.modules.restaurants.schemas.category import CategoryRead, CategoryCreate, CategoryUpdate

class CategoryService:

    def __init__(self, repo: ICategoryRepository, session: AsyncSession):
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
        categories = await self._repo.get_all(restaurant_id, limit, offset)
        return [CategoryRead.model_validate(c) for c in categories]

    async def get_by_id_public(self, category_id: int, restaurant_id: int):
        category = await self._repo.get_by_id(category_id, restaurant_id)

        if not category:
            raise ResourceNotFoundException("Category not found")

        return CategoryRead.model_validate(category)

    # 🔒 PRIVATE
    async def get_all_private(self, restaurant_id: int, user_id: int, limit: int = 10, offset: int = 0):
        await self._check_owner(restaurant_id, user_id)

        return await self.get_all_public(restaurant_id, limit, offset)

    async def get_by_id_private(self, category_id: int, restaurant_id: int, user_id: int):
        await self._check_owner(restaurant_id, user_id)

        return await self.get_by_id_public(category_id, restaurant_id)

    async def create(self, data: CategoryCreate, restaurant_id: int, user_id: int):
        await self._check_owner(restaurant_id, user_id)

        category = Category(**data.model_dump(), restaurant_id=restaurant_id)

        category = await self._repo.create(category)
        await self._session.commit()

        return CategoryRead.model_validate(category)

    async def update(self, category_id: int, restaurant_id: int, user_id: int, data: CategoryUpdate):
        await self._check_owner(restaurant_id, user_id)

        category = await self._repo.get_by_id(category_id, restaurant_id)
        if not category:
            raise ResourceNotFoundException("Category not found")

        payload = data.model_dump(exclude_unset=True)
        category = await self._repo.update(category, payload)

        await self._session.commit()
        return CategoryRead.model_validate(category)

    async def delete(self, category_id: int, restaurant_id: int, user_id: int):
        await self._check_owner(restaurant_id, user_id)

        category = await self._repo.get_by_id(category_id, restaurant_id)
        if not category:
            raise ResourceNotFoundException("Category not found")

        await self._repo.delete(category)
        await self._session.commit()