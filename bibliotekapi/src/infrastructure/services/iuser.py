"""A module containing user service abstractions"""

from abc import ABC, abstractmethod

from pydantic import UUID4, EmailStr

from src.core.domain.user import UserCreate
from src.infrastructure.dto.userdto import UserDTO
from src.infrastructure.dto.tokendto import TokenDTO


class IUserService(ABC):
    """An abstarct repository class for user."""

    @abstractmethod
    async def get_all_users(self) -> list[UserDTO]:
       """The abstract getting all users from the repository (Intended for Librarian use).
        
        Returns:
            list[UserDTO]: The collection of the all users.
        """

    @abstractmethod
    async def get_user_by_uuid(self, user_id: UUID4) -> UserDTO | None:
        """The abstract getting a user from the repository.

        Args:
            user_id (UUID4): The id of the user.
        
        Returns:
            UserDTO | None: The user data if exists.
        """

    @abstractmethod
    async def get_user_by_email(self, email: EmailStr) -> UserDTO | None:
        """The abstract getting a user by email from the repository.

        Args:
            email (EmailStr): The email of the user.
        
        Returns:
            UserDTO | None: The user data if exists.
        """

    @abstractmethod
    async def get_user_by_username(self, username: str) -> UserDTO | None:
        """The abstract getting a user by username from the repository.

        Args:
            username (str): The username of the user.
        
        Returns:
            UserDTO | None: The user data if exists.
        """

    @abstractmethod
    async def register_user(self, data: UserCreate) -> UserDTO | None:
        """The abstract registering a new user.
        
        Args:
            data (UserCreate): The attributes of the user.
        Returns:
            UserDTO | None: The newly registered user.
        """

    @abstractmethod
    async def update_user_email(self, user_id: UUID4, new_email: EmailStr ) -> UserDTO | None:
        """The abstarct updating user email.
        
        Args:
            user_id (UUID4): The user id.
            new_email (EmailStr): The new user email.

        Returns:
            UserDTO | None: The updated user record.
        """

    @abstractmethod
    async def change_user_password(self, user_id: UUID4, new_password: str) -> UserDTO | None:
        """The abstarct changing user password.
        
        Args:
            user_id (UUID4): The user id.
            new password (str): The new user password.

        Returns:
            UserDTO | None: The updated user record.
        """

    @abstractmethod
    async def authenticate_user(self, user: UserCreate) -> TokenDTO | None:
        """The method authenticating the user.

        Args:
            user (UserCreate): The user data.

        Returns:
            TokenDTO | None: The token details.
        """

    @abstractmethod
    async def remove_user(self, user_id: UUID4) -> bool:
        """The abstarct removing user from the repository.

        Args:
            user_id (UUID4): The user id.

        Returns:
            bool: Success of the operation.
        """
    