from typing import Any
from pydantic import BaseModel, ConfigDict, Field, HttpUrl

class RestaurantRead(BaseModel):
    id: int
    slug: str
    name: str
    description: str | None = None
    logo_url: HttpUrl | None = None
    settings: dict[str, Any] | None = None

    model_config = ConfigDict(from_attributes=True)

class RestaurantCreate(BaseModel):
    name: str
    description: str | None = None
    settings: dict[str, Any] | None = None
    
class RestaurantUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=100)
    description: str | None = None
    settings: dict[str, Any] | None = None