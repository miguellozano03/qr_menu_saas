from typing import List
from fastapi import APIRouter, Depends
from app.shared.dependencies.auth import get_current_user_id
from app.modules.restaurants.schemas.link import (
    RestaurantLinkRead,
    RestaurantLinkCreate,
    RestaurantLinkUpdate,
)
from app.modules.restaurants.dependencies import get_links_service


router = APIRouter(prefix="/restaurants/{restaurant_id}/links", tags=["Links"])


@router.get("", response_model=List[RestaurantLinkRead])
async def get_links(
    restaurant_id: int,
    user_id: int = Depends(get_current_user_id),
    service=Depends(get_links_service),
):
    return await service.get_all(restaurant_id, user_id)

@router.post("", response_model=RestaurantLinkRead)
async def create_link(
    restaurant_id: int,
    data: RestaurantLinkCreate,
    user_id: int = Depends(get_current_user_id),
    service=Depends(get_links_service),
):
    return await service.create(data, restaurant_id, user_id)


@router.patch("/{link_id}", response_model=RestaurantLinkRead)
async def update_link(
    restaurant_id: int,
    link_id: int,
    data: RestaurantLinkUpdate,
    user_id: int = Depends(get_current_user_id),
    service=Depends(get_links_service),
):
    return await service.update(link_id, restaurant_id, user_id, data)


@router.delete("/{link_id}")
async def delete_link(
    restaurant_id: int,
    link_id: int,
    user_id: int = Depends(get_current_user_id),
    service=Depends(get_links_service),
):
    return await service.delete(link_id, restaurant_id, user_id)