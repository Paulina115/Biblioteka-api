"""Module containing user service implementation"""

from pydantic import UUID4, EmailStr

from src.core.domain.user import UserCreate
from src.core.repositories.iuser import IUserRepository
from src.infrastructure.services.iuser import IUserService
from src.infrastructure.dto.userdto import UserDTO
from src.infrastructure.dto.tokendto import TokenDTO
from src.infrastructure.utils.password import verify_password
from src.infrastructure.utils.token import generate_user_token


class UserService(IUserService):
    """A class implementing the user service"""

    _repository: IUserRepository

    def __init__(self, repository: IUserRepository):
        self._repository = repository

    async def get_all_users(self) -> list[UserDTO]:
       """The method getting all users from the repository (Intended for Librarian use).
        
        Returns:
            list[UserDTO]: The collection of the all users.
        """
       users = await self._repository.get_all_users()
       return [UserDTO.model_validate(user) for user in users]

    async def get_user_by_uuid(self, user_id: UUID4) -> UserDTO | None:
        """The method getting a user from the repository.

        Args:
            user_id (UUID4): The id of the user.
        
        Returns:
            UserDTO | None: The user data if exists.
        """
        user = await self._repository.get_user_by_uuid(user_id)
        return UserDTO.model_validate(user) if user else None

    async def get_user_by_email(self, email: EmailStr) -> UserDTO | None:
        """The method getting a user by email from the repository.

        Args:
            email (EmailStr): The email of the user.
        
        Returns:
            UserDTO | None: The user data if exists.
        """
        user = await self._repository.get_user_by_email(email)
        return UserDTO.model_validate(user) if user else None


    async def get_user_by_username(self, username: str) -> list[UserDTO]:
        """The method getting a user by username from the repository.

        Args:
            username (str): The username of the user.
        
        Returns:
            list[UserDTO]: The collection of user data.
        """
        users = await self._repository.get_user_by_username(username)
        return [UserDTO.model_validate(user) for user in users]


    async def register_user(self, data: UserCreate) -> UserDTO | None:
        """The method registering a new user.
        
        Args:
            data (UserCreate): The attributes of the user.
        Returns:
            UserDTO | None: The newly registered user.
        """
        if await self._repository.get_user_by_email(data.email):
            return None
        user = await self._repository.add_user(data)
        return UserDTO.model_validate(user) if user else None

    async def update_user_email(self, user_id: UUID4, new_email: EmailStr ) -> UserDTO | None:
        """The method updating user email.
        
        Args:
            user_id (UUID4): The user id.
            new_email (EmailStr): The new user email.

        Returns:
            UserDTO | None: The updated user record.
        """

    async def change_user_password(self, user_id: UUID4, new_password: str) -> UserDTO | None:
        """The method changing user password.
        
        Args:
            user_id (UUID4): The user id.
            new password (str): The new user password.

        Returns:
            UserDTO | None: The updated user record.
        """

    async def authenticate_user(self, user: UserCreate) -> TokenDTO | None:
        """The method authenticating the user.

        Args:
            user (UserCreate): The user data.

        Returns:
            TokenDTO | None: The token details.
        """
        if user_data := await self._repository.get_user_by_email(user.email):
            if verify_password(user.password, user_data.password):
                token_details = generate_user_token(user_data.id)
                # trunk-ignore(bandit/B106)
                return TokenDTO(token_type="Bearer", **token_details)

            return None

        return None


