import json
from decimal import Decimal
from fastapi import APIRouter, Depends, UploadFile, File, Form, UploadFile
from typing import List
from fastapi import APIRouter, Depends
from app.shared.dependencies.auth import get_current_user_id
from app.modules.restaurants.services.product import ProductService
from app.modules.restaurants.schemas.product import (
    ProductRead,
    ProductCreate,
    ProductUpdate,
)
from app.modules.restaurants.dependencies import get_product_service


router = APIRouter(
    prefix="/restaurants/{restaurant_id}/products",
    tags=["Products"],
)


@router.get("", response_model=List[ProductRead])
async def get_products(
    restaurant_id: int,
    user_id: int = Depends(get_current_user_id),
    limit: int = 10,
    offset: int = 0,
    service: ProductService = Depends(get_product_service),
):
    return await service.get_all(restaurant_id, user_id, limit, offset)


@router.get("/{product_id}", response_model=ProductRead)
async def get_product(
    restaurant_id: int,
    product_id: int,
    user_id: int = Depends(get_current_user_id),
    service: ProductService = Depends(get_product_service),
):
    return await service.get_by_id(product_id, restaurant_id, user_id)

@router.post("", response_model=ProductRead)
async def create_product(
    restaurant_id: int,
    category_id: int = Form(...),
    name: str = Form(...),
    description: str | None = Form(None),
    price: Decimal = Form(...),
    is_available: bool = Form(True),
    position: int | None = Form(None),
    image_file: UploadFile = File(None),
    
    user_id: int = Depends(get_current_user_id),
    service: ProductService = Depends(get_product_service),
):
    data = ProductCreate(
        category_id=category_id,
        name=name,
        description=description,
        price=price,
        is_available=is_available,
        position=position
    )
    
    return await service.create(data, restaurant_id, user_id, image_file)


@router.patch("/{product_id}", response_model=ProductRead)
async def update_product(
    restaurant_id: int,
    product_id: int,
    category_id: int | None = Form(None),
    name: str | None = Form(None),
    description: str | None = Form(None),
    price: Decimal | None = Form(None),
    is_available: bool | None = Form(None),
    position: int | None = Form(None),
    image_file: UploadFile = File(None),
    user_id: int = Depends(get_current_user_id),
    service: ProductService = Depends(get_product_service),
):
    data = ProductUpdate(**{
        k: v for k, v in {
            "category_id": category_id,
            "name": name,
            "description": description,
            "price": price,
            "is_available": is_available,
            "position": position,
        }.items() if v is not None
    })
    
    return await service.update(data, product_id, restaurant_id, user_id, image_file)


@router.delete("/{product_id}")
async def delete_product(
    restaurant_id: int,
    product_id: int,
    user_id: int = Depends(get_current_user_id),
    service: ProductService = Depends(get_product_service),
):
    return await service.delete(product_id, restaurant_id, user_id)