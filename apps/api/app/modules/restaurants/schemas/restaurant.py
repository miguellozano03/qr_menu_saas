from typing import Any
from pydantic import BaseModel, ConfigDict, Field, HttpUrl


class RestaurantBase(BaseModel):
    name: str = Field(min_length=1, max_length=100, description="Restaurant Name")
    description: str | None = Field(default=None, min_length=1, max_length=500, description="Restaurant Description")
    logo_url: HttpUrl | None = Field(default=None, max_length=255, description="Restaurant logo url")
    settings: dict[str, Any] | None = Field(default=None, description="Json file to save restaurant settings")

class RestaurantRead(RestaurantBase):
    id: int 
    slug: str = Field(min_length=1, max_length=100, description="Unique Restaurant Slug")
    model_config = ConfigDict(from_attributes=True)

class RestaurantCreate(RestaurantBase):
    pass

class RestaurantUpdate(BaseModel):
     name: str | None = Field(default=None, min_length=1, max_length=100)
