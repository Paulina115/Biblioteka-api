"""A repository for user entity."""

from abc import ABC, abstractmethod
from uuid import UUID

from src.core.domain.user import User, UserCreate


class IUserRepository(ABC):
    """An abstarct repository class for user."""

    @abstractmethod
    async def get_all_users(self) -> list[User]:
       """The abstract getting all users from the data storage.
        
        Returns:
            list[User]: The collection of the all users.
        """

    @abstractmethod
    async def get_user_by_uuid(self, user_id: UUID) -> User | None:
        """The abstract getting a user from the data storage.

        Args:
            user_id (UUID): The id of the user.
        
        Returns:
            User | None: The user data if exists.
        """

    @abstractmethod
    async def get_user_by_email(self, email: str) -> User | None:
        """The abstract getting a user by email from the data storage.

        Args:
            email (str): The email of the user.
        
        Returns:
            User | None: The user data if exists.
        """

    @abstractmethod
    async def get_user_by_username(self, username: str) -> list[User]:
        """The abstract getting a user by username from the data storage.

        Args:
            username (str): The username of the user.
        
        Returns:
            list[User]: The collection of users data.
        """

    @abstractmethod
    async def add_user(self, data: UserCreate) -> User | None:
        """The abstract adding new user to the data storage.
        
        Args:
            data (UserCreate): The attributes of the user.
        Returns:
            User | None: The newly created user.
        """

    @abstractmethod
    async def update_user(self, user_id: UUID, data: UserCreate) -> User | None:
        """The abstarct updating user data in the data storage.
        
        Args:
            user_id (UUID): The user id.
            data (UserCreate): The attributes of the user.

        Returns:
            User | None: The updated user.
        """

    @abstractmethod
    async def delete_user(self, user_id: UUID) -> bool:
        """The abstarct removing user from the data storage.

        Args:
            user_id (UUID): The user id.

        Returns:
            bool: Success of the operation.
        """
    
