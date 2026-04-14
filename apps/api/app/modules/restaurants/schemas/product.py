from decimal import Decimal
from pydantic import BaseModel, ConfigDict, Field

class ProductBase(BaseModel):
    category_id: int = Field(description="ID of the category this product belongs to")
    name: str = Field(min_length=1, max_length=100, description="Product name")
    description: str | None = Field(default=None, min_length=1, max_length=500, description="Product description")
    price: Decimal = Field(gt=0, max_digits=10, decimal_places=2, description="Product price")
    image_url: str | None = Field(default=None, min_length=1, max_length=255, description="Product image URL")
    is_available: bool = Field(default=True, description="Whether the product is available")
    position: int | None = Field(default=None, ge=0, description="Position of the product")

class ProductRead(ProductBase):
    id: int
    restaurant_id: int
    model_config = ConfigDict(from_attributes=True)

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    category_id: int | None = Field(default=None)
    name: str | None = Field(default=None, min_length=1, max_length=100)
    description: str | None = Field(default=None, min_length=1, max_length=500)
    price: Decimal | None = Field(default=None, gt=0, max_digits=10, decimal_places=2)
    image_url: str | None = Field(default=None, min_length=1, max_length=255)
    is_available: bool | None = Field(default=None)
    position: int | None = Field(default=None, ge=0)