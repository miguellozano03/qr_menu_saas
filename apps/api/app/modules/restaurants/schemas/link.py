from pydantic import BaseModel, ConfigDict, Field
from app.shared.enums import LinkType


class RestaurantLinkBase(BaseModel):
    type: LinkType | None = Field(default=None, description="Type of the link")
    url: str | None = Field(default=None, min_length=1, max_length=500, description="URL of the link")
    position: int | None = Field(default=None, ge=0, description="Position of the link")

class RestaurantLinkRead(RestaurantLinkBase):
    id: int
    restaurant_id: int
    model_config = ConfigDict(from_attributes=True)

class RestaurantLinkCreate(RestaurantLinkBase):
    pass

class RestaurantLinkUpdate(BaseModel):
    type: LinkType | None = Field(default=None)
    url: str | None = Field(default=None, min_length=1, max_length=500)
    position: int | None = Field(default=None, ge=0)