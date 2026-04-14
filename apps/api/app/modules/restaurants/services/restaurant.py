import re
import unicodedata
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.exceptions import ResourceNotFoundException
from app.modules.restaurants.schemas.restaurant import (
    RestaurantRead,
    RestaurantCreate,
    RestaurantUpdate
)
from app.modules.restaurants.repositories.restaurant import IRestaurantRepository
from app.modules.restaurants.models import Restaurant


def _slugify(text: str) -> str:
    text = unicodedata.normalize("NFKD", text)
    text = text.encode("ascii", "ignore").decode("ascii")
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_-]+", "-", text)
    text = re.sub(r"^-+|-+$", "", text)
    return text


class RestaurantService:

    def __init__(self, repo: IRestaurantRepository, session: AsyncSession):
        self._repo = repo
        self._session = session

    # ---------- PUBLIC ----------
    async def get_all(self, limit: int, offset: int):
        restaurants = await self._repo.get_all(limit, offset)
        return [RestaurantRead.model_validate(r) for r in restaurants]

    async def get_public_by_slug(self, slug: str):
        restaurant = await self._repo.get_by_slug(slug)

        if not restaurant:
            raise ResourceNotFoundException("Restaurant not found")

        return RestaurantRead.model_validate(restaurant)

    # ---------- PRIVATE ----------
    async def get_private_by_slug(self, slug: str, user_id: int):
        restaurant = await self._repo.get_by_slug(slug)

        if not restaurant or restaurant.owner_id != user_id:
            raise ResourceNotFoundException("Restaurant not found")

        return RestaurantRead.model_validate(restaurant)

    async def get_by_id_private(self, restaurant_id: int, user_id: int):
        restaurant = await self._repo.get_by_id(restaurant_id)

        if not restaurant or restaurant.owner_id != user_id:
            raise ResourceNotFoundException("Restaurant not found")

        return RestaurantRead.model_validate(restaurant)

    # ---------- CREATE ----------
    async def create(self, data: RestaurantCreate, owner_id: int):
        slug = await self._generate_unique_slug(data.name)

        restaurant = Restaurant(
            owner_id=owner_id,
            slug=slug,
            name=data.name,
            description=data.name,
            logo_url=str(data.logo_url) if data.logo_url else None,
            settings=data.settings
        )

        restaurant = await self._repo.create(restaurant)
        return RestaurantRead.model_validate(restaurant)

    # ---------- UPDATE ----------
    async def update(self, restaurant_id: int, user_id: int, data: RestaurantUpdate):
        restaurant = await self._repo.get_by_id(restaurant_id)

        if not restaurant or restaurant.owner_id != user_id:
            raise ResourceNotFoundException("Restaurant not found")

        payload = data.model_dump(exclude_unset=True)

        if "name" in payload and payload["name"] != restaurant.name:
            payload["slug"] = await self._generate_unique_slug(payload["name"])

        restaurant = await self._repo.update(restaurant, payload)
        await self._session.commit()

        return RestaurantRead.model_validate(restaurant)

    # ---------- DELETE ----------
    async def delete(self, restaurant_id: int, user_id: int):
        restaurant = await self._repo.get_by_id(restaurant_id)

        if not restaurant or restaurant.owner_id != user_id:
            raise ResourceNotFoundException("Restaurant not found")

        await self._repo.delete(restaurant)

    # ---------- INTERNAL ----------
    async def _generate_unique_slug(self, name: str) -> str:
        base_slug = _slugify(name)
        slug = base_slug
        counter = 2

        while await self._repo.get_by_slug(slug):
            slug = f"{base_slug}-{counter}"
            counter += 1

        return slug