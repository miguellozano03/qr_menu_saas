from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db.database import get_db
from .service import PublicMenuService
from .repository import PublicMenuRepository

async def get_restaurant_menu_service(session: AsyncSession = Depends(get_db)):
    return PublicMenuService(
        repo=PublicMenuRepository(session),
        session=session
    )