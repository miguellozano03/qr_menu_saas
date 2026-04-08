from __future__ import annotations
from typing import TYPE_CHECKING
from sqlalchemy import String, BigInteger, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db.base import Base
from app.core.db.mixins import TimestampMixin
if TYPE_CHECKING:
    from app.modules.restaurants.models import Restaurant

class User(TimestampMixin, Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)

    restaurants: Mapped[list["Restaurant"]] = relationship("Restaurant", back_populates="owner")