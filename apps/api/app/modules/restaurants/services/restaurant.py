import re
import unicodedata
from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from app.core.exceptions import ResourceNotFoundException, IsDuplicatedException
from app.modules.restaurants.schemas.restaurant import (
    RestaurantRead,
    RestaurantCreate,
    RestaurantUpdate
)
from app.shared.storage.base import StorageService
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

    def __init__(self, repo: IRestaurantRepository, storage: StorageService, session: AsyncSession):
        self._repo = repo
        self._session = session
        self._storage = storage

    async def _get_owned(self, restaurant_id: int, user_id: int) -> Restaurant:
        restaurant = await self._repo.get_by_id(restaurant_id)

        if restaurant is None or restaurant.owner_id != user_id:
            raise ResourceNotFoundException("Restaurant not found")

        return restaurant

    async def get_all(self, user_id: int, limit: int = 10, offset: int = 0):
        restaurants = await self._repo.get_all(limit, offset)

        return [
            RestaurantRead.model_validate(r)
            for r in restaurants
            if r.owner_id == user_id
        ]

    async def get_by_id(self, restaurant_id: int, user_id: int):
        restaurant = await self._get_owned(restaurant_id, user_id)
        return RestaurantRead.model_validate(restaurant)

    async def get_by_slug(self, slug: str, user_id: int):
        restaurant = await self._repo.get_by_slug(slug)

        if restaurant is None or restaurant.owner_id != user_id:
            raise ResourceNotFoundException("Restaurant not found")

        return RestaurantRead.model_validate(restaurant)

    async def create(self, data: RestaurantCreate, user_id: int, logo_file: UploadFile | None = None):
        slug = await self._generate_unique_slug(data.name)
        
        logo_url = None
        if logo_file:
            logo_url = await self._storage.upload(logo_file)
            
        restaurant = Restaurant(
            owner_id=user_id,
            slug=slug,
            name=data.name,
            description=data.description,
            logo_url=logo_url,
            settings=data.settings,
        )
        
        try:
            created = await self._repo.create(restaurant)
            await self._session.commit()
        except IntegrityError:
            await self._session.rollback()
            raise IsDuplicatedException("Slug already exists")

        return RestaurantRead.model_validate(created)

    async def update(self, restaurant_id: int, user_id: int, data: RestaurantUpdate, logo_file: UploadFile | None = None):
        restaurant = await self._get_owned(restaurant_id, user_id)

        payload = data.model_dump(exclude_unset=True)

        new_name = payload.get("name")
        if new_name and new_name != restaurant.name:
            payload["slug"] = await self._generate_unique_slug(new_name)

        if logo_file:
            payload["logo_url"] = await self._storage.upload(logo_file)

        payload = {k: v for k, v in payload.items() if v is not None}

        updated = await self._repo.update(restaurant, payload)
        await self._session.commit()

        return RestaurantRead.model_validate(updated)

    async def delete(self, restaurant_id: int, user_id: int):
        restaurant = await self._get_owned(restaurant_id, user_id)

        await self._repo.delete(restaurant)
        await self._session.commit()

    async def _generate_unique_slug(self, name: str) -> str:
        base = _slugify(name)
        slug = base
        counter = 2

        while await self._repo.get_by_slug(slug):
            slug = f"{base}-{counter}"
            counter += 1

        return slug