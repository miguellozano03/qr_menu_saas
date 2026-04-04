from __future__ import annotations
from decimal import Decimal
from typing import TYPE_CHECKING
from sqlalchemy import String, Text, BigInteger, Integer, Numeric, Boolean, ForeignKey, Index, Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import JSONB

from app.core.db.base import Base
from app.core.db.mixins import TimestampMixin
from app.shared.enums import LinkType
if TYPE_CHECKING:
    from app.modules.users.models import User

class Restaurant(TimestampMixin, Base):
    __tablename__ = 'restaurants'
    __table_args__ = (
    Index("ix_restaurant_owner_deleted", "owner_id", "deleted_at"),
    )
        
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True, nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    slug: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
    logo_url: Mapped[str | None] = mapped_column(String(255), nullable=True)
    settings: Mapped[dict | None] = mapped_column(JSONB, nullable=True)

    owner: Mapped["User"] = relationship("User", back_populates="restaurants")
    links: Mapped[list["RestaurantLink"]] = relationship("RestaurantLink", back_populates="restaurant")
    categories: Mapped[list["Category"]] = relationship("Category", back_populates="restaurant")
    products: Mapped[list["Product"]] = relationship("Product", back_populates="restaurant")


class RestaurantLink(TimestampMixin, Base):
    __tablename__ = 'restaurant_links'
    __table_args__ = (
        Index("ix_restaurant_links_restaurant_type", "restaurant_id", "type"),
    )
        
    
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    restaurant_id: Mapped[int] = mapped_column(ForeignKey("restaurants.id"), index=True, nullable=False)
    type: Mapped[LinkType | None] = mapped_column(SAEnum(LinkType), nullable=True)
    url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    position: Mapped[int | None] = mapped_column(Integer, nullable=True)

    restaurant: Mapped["Restaurant"] = relationship("Restaurant", back_populates="links")

class Category(TimestampMixin, Base):
    __tablename__ = "categories"
    __table_args__ = (
        Index("ix_categories_restaurant_position", "restaurant_id", "position"),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    restaurant_id: Mapped[int] = mapped_column(ForeignKey("restaurants.id"), index=True, nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    position: Mapped[int | None] = mapped_column(Integer, nullable=True)

    restaurant: Mapped["Restaurant"] = relationship("Restaurant", back_populates="categories")
    products: Mapped[list["Product"]] = relationship("Product", back_populates="category")

class Product(TimestampMixin, Base):
    __tablename__ = "products"

    __table_args__ = (
        Index("ix_product_restaurant_deleted", "restaurant_id", "deleted_at"),
        Index("ix_product_restaurant_category", "restaurant_id", "category_id"),
        Index("ix_product_category_position", "category_id", "position"),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    restaurant_id: Mapped[int] = mapped_column(ForeignKey("restaurants.id"), index=True, nullable=False)
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"), index=True, nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    price: Mapped[Decimal] = mapped_column(Numeric(10,2), nullable=False)
    image_url: Mapped[str | None] = mapped_column(String(255), nullable=True)
    is_available: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    position: Mapped[int | None] = mapped_column(Integer, nullable=True)


    restaurant: Mapped["Restaurant"] = relationship("Restaurant", back_populates="products")
    category: Mapped["Category"] = relationship("Category", back_populates="products")