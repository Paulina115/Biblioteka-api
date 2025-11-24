from typing import Any, Iterable

from sqlalchemy import select,join

from core.repositories.iuser import IUserRepository
from core.domain.user import User


class UserRepository(IUserRepository):

    async def get_all_users(self) -> Iterable[User]:
        pass

    async def get_user_by_id(self, id: int) -> User:
        pass

    async def get_user_by_email(self, email: str) -> User:
        pass

    async def create_user(self, data: User) -> None:
        pass

    async def delete_user(self, id: int) -> None:
        pass
    
