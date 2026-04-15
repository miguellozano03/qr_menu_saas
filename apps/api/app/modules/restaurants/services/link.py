from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.restaurants.schemas.link import (
    RestaurantLinkRead,
    RestaurantLinkCreate,
    RestaurantLinkUpdate,
)
from app.modules.restaurants.repositories.link import IRestaurantLinkRepository
from app.modules.restaurants.models import Restaurant, RestaurantLink
from app.core.exceptions import ResourceNotFoundException


class RestaurantLinkService:

    def __init__(self, repo: IRestaurantLinkRepository, session: AsyncSession):
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

        links = await self._repo.get_all(restaurant_id, limit, offset)
        return [RestaurantLinkRead.model_validate(l) for l in links]

    async def get_by_id(self, link_id: int, restaurant_id: int, user_id: int):
        await self._check_owner(restaurant_id, user_id)

        link = await self._repo.get_by_id(link_id, restaurant_id)

        if link is None:
            raise ResourceNotFoundException("Restaurant link not found")

        return RestaurantLinkRead.model_validate(link)

    async def create(self, data: RestaurantLinkCreate, restaurant_id: int, user_id: int):
        await self._check_owner(restaurant_id, user_id)

        link = RestaurantLink(**data.model_dump(), restaurant_id=restaurant_id)

        created = await self._repo.create(link, restaurant_id)
        await self._session.commit()

        return RestaurantLinkRead.model_validate(created)

    async def update(self, link_id: int, restaurant_id: int, user_id: int, data: RestaurantLinkUpdate):
        await self._check_owner(restaurant_id, user_id)

        link = await self._repo.get_by_id(link_id, restaurant_id)

        if link is None:
            raise ResourceNotFoundException("Restaurant link not found")

        updated = await self._repo.update(link, data.model_dump(exclude_unset=True))
        await self._session.commit()

        return RestaurantLinkRead.model_validate(updated)

    async def delete(self, link_id: int, restaurant_id: int, user_id: int):
        await self._check_owner(restaurant_id, user_id)

        link = await self._repo.get_by_id(link_id, restaurant_id)

        if link is None:
            raise ResourceNotFoundException("Restaurant link not found")

        await self._repo.delete(link)
        await self._session.commit()