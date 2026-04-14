from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db.database import get_db
from app.modules.restaurants.repositories.restaurant import RestaurantRepository
from app.modules.restaurants.services.restaurant import RestaurantService
from app.modules.restaurants.repositories.restaurant_link import RestaurantLinkRepository
from app.modules.restaurants.services.restaurant_link import RestaurantLinkService
from app.modules.restaurants.repositories.category import CategoryRepository
from app.modules.restaurants.services.category import CategoryService
from app.modules.restaurants.repositories.product import ProductRepository
from app.modules.restaurants.services.product import ProductService


async def get_restaurant_service(session: AsyncSession = Depends(get_db)):
    return RestaurantService(
        repo=RestaurantRepository(session),
        session=session   
    )
    
async def get_links_service(session: AsyncSession = Depends(get_db)):
    return RestaurantLinkService(
        repo=RestaurantLinkRepository(session),
        session=session
    )

async def get_category_service(session: AsyncSession = Depends(get_db)):
    return CategoryService(
        repo=CategoryRepository(session),
        session=session
    )

async def get_product_service(session: AsyncSession = Depends(get_db)):
    return ProductService(
        repo=ProductRepository(session),
        session=session
    )