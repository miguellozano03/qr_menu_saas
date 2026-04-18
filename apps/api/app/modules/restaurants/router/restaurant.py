import json
from fastapi import APIRouter, Depends, UploadFile, File, Form
from app.core.exceptions import InvalidFile
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


@router.post("/", response_model=RestaurantRead)
async def create(
    name: str = Form(...),
    description: str | None = Form(None),
    settings: str | None = Form(None),
    logo_file: UploadFile | None = File(None),
    current_user_id: int = Depends(get_current_user_id),
    service: RestaurantService = Depends(get_restaurant_service),
):
    try:
        parsed_settings = json.loads(settings) if settings else None
    except json.JSONDecodeError:
        raise InvalidFile("Settings must be a valid json")

    data = RestaurantCreate(
        name=name,
        description=description,
        settings=parsed_settings,
    )
    return await service.create(data, current_user_id, logo_file)


@router.patch("/{restaurant_id}", response_model=RestaurantRead)
async def update(
    restaurant_id: int,
    name: str | None = Form(None),
    description: str | None = Form(None),
    settings: str | None = Form(None),
    logo_file: UploadFile | None = File(None),
    current_user_id: int = Depends(get_current_user_id),
    service: RestaurantService = Depends(get_restaurant_service),
):
    try:
        parsed_settings = json.loads(settings) if settings else None
    except json.JSONDecodeError:
        raise InvalidFile("Settings must be a valid json")

    data = RestaurantUpdate(
        name=name,
        description=description,
        settings=parsed_settings,
    )
    return await service.update(restaurant_id, current_user_id, data, logo_file)