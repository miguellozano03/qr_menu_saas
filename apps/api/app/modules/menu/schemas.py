from decimal import Decimal
from typing import Any
from pydantic import BaseModel, ConfigDict, Field, field_serializer
from app.shared.enums import LinkType

class PublicLinkRead(BaseModel):
    type: LinkType | None
    url: str | None
    position: int | None
    
    model_config = ConfigDict(from_attributes=True)
    
    
class PublicProductRead(BaseModel):
    id: int
    name: str
    description: str | None
    price: Decimal
    image_url: str | None
    is_available: bool
    position: int | None    
    
    @field_serializer("price")
    def serialize_price(self, value: Decimal):
        return float(value)
    
    model_config = ConfigDict(from_attributes=True)
    
class PublicCategoryRead(BaseModel):
    id: int
    name: str
    position: int | None = None
    products: list[PublicProductRead]
    
    model_config = ConfigDict(from_attributes=True)
    
class PublicRestaurantProfile(BaseModel):
    name: str
    description: str | None
    logo_url: str | None
    slug: str
    links: list[PublicLinkRead] = Field(default_factory=list)
    
    model_config = ConfigDict(from_attributes=True)
    
class PublicMenuRead(BaseModel):
    name: str
    logo_url: str | None
    categories: list[PublicCategoryRead] = Field(default_factory=list)
    
    model_config = ConfigDict(from_attributes=True)