from typing import List
from fastapi import APIRouter, Depends
from app.shared.dependencies.auth import get_current_user_id
from app.modules.restaurants.services.restaurant import RestaurantService
from app.modules.restaurants.schemas import RestaurantRead, RestaurantCreate, RestaurantUpdate
from .dependencies import get_restaurant_service

restaurant_router = APIRouter(prefix="/restaurants", tags=["Restaurants"])

@restaurant_router.get("", response_model=List[RestaurantRead], summary="Get all restaurants belonging to an user")
async def get_restaurants(
    limit: int = 10, offset: int = 0,
    current_user_id: int = Depends(get_current_user_id),
    service: RestaurantService = Depends(get_restaurant_service)
):
    return await service.get_all(user_id=current_user_id, limit=limit, offset=offset)

@restaurant_router.get("/{slug}", response_model=RestaurantRead, summary="Get one restaurant by slug",)
async def get_restaurant_by_slug(
    slug: str, current_user_id: int = Depends(get_current_user_id),
    service: RestaurantService = Depends(get_restaurant_service)
):
    return await service.get_by_slug(slug=slug, user_id=current_user_id)

@restaurant_router.post("", response_model=RestaurantRead, summary="Create a new restaurant belonging to the account user")
async def create_restaurant(
    data: RestaurantCreate,
    current_user_id: int = Depends(get_current_user_id),
    service: RestaurantService = Depends(get_restaurant_service)
):
    return await service.create(data, owner_id=current_user_id)

@restaurant_router.patch("/{restaurant_id}", response_model=RestaurantRead, summary="Update a restaurant belonging to the account user")
async def update_restaurant(
    restaurant_id: int,
    data: RestaurantUpdate,
    current_user_id: int = Depends(get_current_user_id),
    service: RestaurantService = Depends(get_restaurant_service)
):
    return await service.update(restaurant_id=restaurant_id, user_id=current_user_id, data=data)

@restaurant_router.delete("", summary="Delete a restaurant belonging to the accoount user")
async def delete_restaurant(
    restaurant_id: int,
    current_user_id: int = Depends(get_current_user_id),
    service: RestaurantService = Depends(get_restaurant_service)
):
    return await service.delete(restaurant_id=restaurant_id, user_id=current_user_id)