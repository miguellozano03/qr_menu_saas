from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.restaurants.schemas.link import (
    RestaurantLinkRead,
    RestaurantLinkCreate,
    RestaurantLinkUpdate,
)
from app.modules.restaurants.repositories.restaurant_link import IRestaurantLinkRepository
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

        if not restaurant or restaurant.owner_id != user_id:
            raise ResourceNotFoundException("Restaurant not found")

        return restaurant

    # 🔓 PUBLIC
    async def get_all_public(self, restaurant_id: int, limit: int = 10, offset: int = 0):
        links = await self._repo.get_all(restaurant_id, limit, offset)
        return [RestaurantLinkRead.model_validate(l) for l in links]

    async def get_by_id_public(self, link_id: int, restaurant_id: int):
        link = await self._repo.get_by_id(link_id, restaurant_id)

        if not link:
            raise ResourceNotFoundException("Restaurant link not found")

        return RestaurantLinkRead.model_validate(link)

    # 🔒 PRIVATE
    async def get_all_private(self, restaurant_id: int, user_id: int, limit: int = 10, offset: int = 0):
        await self._check_owner(restaurant_id, user_id)

        links = await self._repo.get_all(restaurant_id, limit, offset)
        return [RestaurantLinkRead.model_validate(l) for l in links]

    async def get_by_id_private(self, link_id: int, restaurant_id: int, user_id: int):
        await self._check_owner(restaurant_id, user_id)

        link = await self._repo.get_by_id(link_id, restaurant_id)

        if not link:
            raise ResourceNotFoundException("Restaurant link not found")

        return RestaurantLinkRead.model_validate(link)

    async def create(self, data: RestaurantLinkCreate, restaurant_id: int, user_id: int):
        await self._check_owner(restaurant_id, user_id)

        link = RestaurantLink(**data.model_dump())
        link.restaurant_id = restaurant_id

        link = await self._repo.create(link, restaurant_id)
        await self._session.commit()

        return RestaurantLinkRead.model_validate(link)

    async def update(self, link_id: int, restaurant_id: int, user_id: int, data: RestaurantLinkUpdate):
        await self._check_owner(restaurant_id, user_id)

        link = await self._repo.get_by_id(link_id, restaurant_id)
        if not link:
            raise ResourceNotFoundException("Restaurant link not found")

        payload = data.model_dump(exclude_unset=True)
        link = await self._repo.update(link, payload)

        await self._session.commit()
        return RestaurantLinkRead.model_validate(link)

    async def delete(self, link_id: int, restaurant_id: int, user_id: int):
        await self._check_owner(restaurant_id, user_id)

        link = await self._repo.get_by_id(link_id, restaurant_id)
        if not link:
            raise ResourceNotFoundException("Restaurant link not found")

        await self._repo.delete(link)
        await self._session.commit()