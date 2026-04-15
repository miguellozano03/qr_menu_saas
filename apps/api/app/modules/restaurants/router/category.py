from typing import List
from fastapi import APIRouter, Depends

from app.shared.dependencies.auth import get_current_user_id
from app.modules.restaurants.services.category import CategoryService
from app.modules.restaurants.schemas.category import (
    CategoryCreate,
    CategoryRead,
    CategoryUpdate,
)
from app.modules.restaurants.dependencies import get_category_service

router = APIRouter(
    prefix="/restaurants/{restaurant_id}/categories",
    tags=["Categories"],
)


@router.get("", response_model=List[CategoryRead])
async def get_categories(
    restaurant_id: int,
    user_id: int = Depends(get_current_user_id),
    limit: int = 10,
    offset: int = 0,
    service: CategoryService = Depends(get_category_service),
):
    return await service.get_all(restaurant_id, user_id, limit, offset)


@router.get("/{category_id}", response_model=CategoryRead)
async def get_category(
    restaurant_id: int,
    category_id: int,
    user_id: int = Depends(get_current_user_id),
    service: CategoryService = Depends(get_category_service),
):
    return await service.get_by_id(category_id, restaurant_id, user_id)


@router.post("", response_model=CategoryRead)
async def create_category(
    restaurant_id: int,
    data: CategoryCreate,
    user_id: int = Depends(get_current_user_id),
    service: CategoryService = Depends(get_category_service),
):
    return await service.create(data, restaurant_id, user_id)


@router.patch("/{category_id}", response_model=CategoryRead)
async def update_category(
    restaurant_id: int,
    category_id: int,
    data: CategoryUpdate,
    user_id: int = Depends(get_current_user_id),
    service: CategoryService = Depends(get_category_service),
):
    return await service.update(category_id, restaurant_id, user_id, data)


@router.delete("/{category_id}")
async def delete_category(
    restaurant_id: int,
    category_id: int,
    user_id: int = Depends(get_current_user_id),
    service: CategoryService = Depends(get_category_service),
):
    return await service.delete(category_id, restaurant_id, user_id)