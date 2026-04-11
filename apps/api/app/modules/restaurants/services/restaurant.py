import re
import unicodedata
from abc import ABC, abstractmethod
from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import ResourceNotFoundException
from app.modules.restaurants.schemas import (
    RestaurantRead,
    RestaurantCreate,
    RestaurantUpdate,
)
from app.modules.restaurants.repositories.restaurant import IRestaurantRepository
from app.modules.restaurants.models import Restaurant


class IRestaurantService(ABC):

    @abstractmethod
    async def get_all(self, user_id: int, limit: int = 10, offset: int = 0) -> Sequence[RestaurantRead]:
        pass

    @abstractmethod
    async def get_by_id(self, restaurant_id: int, user_id: int) -> RestaurantRead:
        pass

    @abstractmethod
    async def get_by_slug(self, slug: str, user_id: int) -> RestaurantRead:
        pass

    @abstractmethod
    async def create(self, data: RestaurantCreate, owner_id: int) -> RestaurantRead:
        pass

    @abstractmethod
    async def update(self, restaurant_id: int, user_id: int, data: RestaurantUpdate) -> RestaurantRead:
        pass

    @abstractmethod
    async def delete(self, restaurant_id: int, user_id: int) -> None:
        pass

def _slugify(text: str) -> str:
    text = unicodedata.normalize("NFKD", text)
    text = text.encode("ascii", "ignore").decode("ascii")
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_-]+", "-", text)
    text = re.sub(r"^-+|-+$", "", text)
    return text

class RestaurantService(IRestaurantService):
    def __init__(self, repo: IRestaurantRepository, session: AsyncSession, ) -> None:
        self._repo = repo
        self._session = session

    async def get_all(self, user_id: int, limit: int = 10, offset: int = 0) -> Sequence[RestaurantRead]:
        restaurants = await self._repo.get_all(user_id, limit, offset)
        return [RestaurantRead.model_validate(restaurant) for restaurant in restaurants]
    
    async def get_by_id(self, restaurant_id: int, user_id: int) -> RestaurantRead:
        restaurant = self._repo.get_by_id(restaurant_id, user_id)

        if not restaurant:
            raise ResourceNotFoundException("Restaurant not found")
        
        return RestaurantRead.model_validate(restaurant)
    
    async def get_by_slug(self, slug: str, user_id: int) -> RestaurantRead:
        restaurant = self._repo.get_by_slug(slug, user_id)

        if not restaurant:
            raise ResourceNotFoundException("Restaurant not found")
                
        return RestaurantRead.model_validate(restaurant)

    async def _generate_unique_slug(self, name: str, user_id: int) -> str:
        base_slug = _slugify(name)
        slug = base_slug
        counter = 2

        while await self._repo.get_by_slug(slug=slug, user_id=user_id):
            slug = f"{base_slug}-{counter}"
            counter += 1

        return slug
    
    async def create(self, data: RestaurantCreate, owner_id: int):
        slug = await self._generate_unique_slug(data.name, owner_id)

        restaurant = Restaurant(
            owner_id = owner_id,
            slug = slug,
            name = data.name,
            description = data.name,
            logo_url = str(data.logo_url) if data.logo_url else None,
            settings= data.settings
        )
        restaurant = await self._repo.create(restaurant)
        return RestaurantRead.model_validate(restaurant)
    
    async def update(self, restaurant_id: int, user_id: int, data: RestaurantUpdate) -> RestaurantRead:

        payload = data.model_dump(exclude_unset=True)

        restaurant = await self._repo.get_by_id(restaurant_id, user_id)

        if not restaurant:
            raise ResourceNotFoundException("Restaurant not found")
        
        new_name = payload.get("name")
        

        if new_name and new_name != restaurant.name:
            payload["slug"] = await self._generate_unique_slug(new_name, user_id)

        restaurant = await self._repo.update(restaurant, payload)

        return RestaurantRead.model_validate(restaurant)
    
    async def delete(self, restaurant_id, user_id: int):
        restaurant = await self._repo.get_by_id(restaurant_id, user_id)

        if not restaurant:
            raise ResourceNotFoundException("Restaurant not found")
        
        await self._repo.delete(restaurant)