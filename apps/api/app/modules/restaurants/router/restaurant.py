from typing import List
from fastapi import APIRouter, Depends
from app.shared.dependencies.auth import get_current_user_id
from app.modules.restaurants.services.restaurant import RestaurantService
from app.modules.restaurants.schemas.restaurant import (
    RestaurantRead,
    RestaurantCreate,
    RestaurantUpdate
)
from app.modules.restaurants.dependencies import get_restaurant_service


router = APIRouter(prefix="/restaurants", tags=["Restaurants"])


@router.get("/{slug}", response_model=RestaurantRead)
async def get_public(
    slug: str,
    current_user_id: int = Depends(get_current_user_id),
    service: RestaurantService = Depends(get_restaurant_service),
):
    return await service.get_by_slug(slug, current_user_id)


@router.get("")
async def get_all(
    limit: int = 10,
    offset: int = 0,
    current_user_id: int = Depends(get_current_user_id),
    service: RestaurantService = Depends(get_restaurant_service),
):
    return await service.get_all(current_user_id, limit, offset)


@router.post("", response_model=RestaurantRead)
async def create(
    data: RestaurantCreate,
    current_user_id: int = Depends(get_current_user_id),
    service: RestaurantService = Depends(get_restaurant_service),
):
    return await service.create(data, current_user_id)


@router.patch("/{restaurant_id}", response_model=RestaurantRead)
async def update(
    restaurant_id: int,
    data: RestaurantUpdate,
    current_user_id: int = Depends(get_current_user_id),
    service: RestaurantService = Depends(get_restaurant_service),
):
    return await service.update(restaurant_id, current_user_id, data)


@router.delete("/{restaurant_id}")
async def delete(
    restaurant_id: int,
    current_user_id: int = Depends(get_current_user_id),
    service: RestaurantService = Depends(get_restaurant_service),
):
    return await service.delete(restaurant_id, current_user_id)