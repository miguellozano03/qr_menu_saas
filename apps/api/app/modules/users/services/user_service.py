from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import ResourceNotFoundException
from app.modules.users.repository import UserRepository
from app.modules.users.schemas import UserRead, UserUpdate


class UserService:
    def __init__(self, repo: UserRepository, session: AsyncSession) -> None:
        self._repo = repo
        self._session = session

    async def get_user_by_id(self, user_id:int):
        user = await self._repo.get_user_by_id(user_id)
        if not user:
            raise ResourceNotFoundException("User not found")
        
        return UserRead.model_validate(user)

    async def update_user(self, user_id: int, data: UserUpdate) -> UserRead:
        user = await self._repo.get_user_by_id(user_id)
        if not user:
            raise ResourceNotFoundException("User not found")
        
        updated = await self._repo.update(user, data)
        await self._session.commit()
        
        return UserRead.model_validate(updated)
        
    async def me(self, user_id: int) -> UserRead:
        user = await self._repo.get_user_by_id(user_id)
        if not user:
            raise ResourceNotFoundException("User not found")
        
        return UserRead.model_validate(user)

    async def delete_account(self, user_id: int) -> None:
        user = await self._repo.get_user_by_id(user_id)
        if not user:
            raise ResourceNotFoundException("User not found")
        
        await self._repo.delete(user)
        await self._session.commit()