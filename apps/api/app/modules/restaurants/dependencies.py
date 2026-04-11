from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db.database import get_db
from app.modules.restaurants.repositories.restaurant import RestaurantRepository
from app.modules.restaurants.services.restaurant import RestaurantService


async def get_restaurant_service(session: AsyncSession = Depends(get_db)):
    return RestaurantService(
        repo=RestaurantRepository(session),
        session=session   
    )