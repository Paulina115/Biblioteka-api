from abc import ABC, abstractmethod
from typing import Iterable

from src.core.domain.user import User


class IUserRepository(ABC):

    @abstractmethod
    async def get_all_users(self) -> Iterable[User]:
        pass

    @abstractmethod
    async def get_user_by_id(self, id: int) -> User:
        pass

    @abstractmethod
    async def get_user_by_email(self, email: str) -> User:
        pass

    @abstractmethod
    async def create_user(self, data: User) -> None:
        pass

    @abstractmethod
    async def delete_user(self, id: int) -> None:
        pass
    
