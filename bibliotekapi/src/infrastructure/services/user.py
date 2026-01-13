"""Module containing user service implementation"""

from pydantic import UUID4, EmailStr

from src.core.domain.user import UserCreate, UserRole, UserLogin
from src.core.repositories.iuser import IUserRepository
from src.infrastructure.services.iuser import IUserService
from src.infrastructure.dto.userdto import UserDTO
from src.infrastructure.dto.tokendto import TokenDTO
from src.infrastructure.utils.password import hash_password
from src.infrastructure.utils.password import verify_password
from src.infrastructure.utils.token import generate_user_token
from src.infrastructure.services.iunit_of_work import IUnitOfWork
from src.core.exceptions.exceptions import EmailAlreadyExist


class UserService(IUserService):
    """A class implementing the user service"""

    def __init__(self, uow: IUnitOfWork):
        self._uow = uow

    async def get_all_users(self) -> list[UserDTO]:
       """The method getting all users from the repository (Intended for Librarian use).
        
        Returns:
            list[UserDTO]: The collection of the all users.
        """
       async with self._uow:
            users = await self._uow.user_repository.get_all_users()
            return [UserDTO.model_validate(user) for user in users]

    async def get_user_by_uuid(self, user_id: UUID4) -> UserDTO | None:
        """The method getting a user from the repository.

        Args:
            user_id (UUID4): The id of the user.
        
        Returns:
            UserDTO | None: The user data if exists.
        """
        async with self._uow:
            user = await self._uow.user_repository.get_user_by_uuid(user_id)
            return UserDTO.model_validate(user) if user else None

    async def get_user_by_email(self, email: EmailStr) -> UserDTO | None:
        """The method getting a user by email from the repository.

        Args:
            email (EmailStr): The email of the user.
        
        Returns:
            UserDTO | None: The user data if exists.
        """
        async with self._uow:
            user = await self._uow.user_repository.get_user_by_email(email)
            return UserDTO.model_validate(user) if user else None


    async def get_user_by_username(self, username: str) -> list[UserDTO]:
        """The method getting a user by username from the repository.

        Args:
            username (str): The username of the user.
        
        Returns:
            list[UserDTO]: The collection of user data.
        """
        async with self._uow:
            users = await self._uow.user_repository.get_user_by_username(username)
            return [UserDTO.model_validate(user) for user in users]


    async def register_user(self, data: UserCreate) -> UserDTO | None:
        """The method registering a new user.
        
        Args:
            data (UserCreate): The attributes of the user.
        Returns:
            UserDTO | None: The newly registered user.
        """
        async with self._uow:
            if await self._uow.user_repository.get_user_by_email(data.email):
                raise EmailAlreadyExist()
            user = await self._uow.user_repository.add_user(data)
            return UserDTO.model_validate(user) if user else None
    
    async def update_user_username(self, user_id: UUID4, username: str ) -> UserDTO | None:
        """The method updating user username.
        
        Args:
            user_id (UUID4): The user id.
            username (str): The updated username.

        Returns:
            UserDTO | None: The updated user record.
        """
        async with self._uow:
            user = await self._uow.user_repository.get_user_by_uuid(user_id=user_id)
            if not user:
                return None
            user.username = username
            updated_user = await self._uow.user_repository.update_user(user_id,user)
            return UserDTO.model_validate(updated_user)

    async def update_user_email(self, user_id: UUID4, new_email: EmailStr ) -> UserDTO | None:
        """The method updating user email.
        
        Args:
            user_id (UUID4): The user id.
            new_email (EmailStr): The new user email.

        Returns:
            UserDTO | None: The updated user record.
        """
        async with self._uow:
            user = await self._uow.user_repository.get_user_by_uuid(user_id=user_id)
            if not user:
                return None
            if await self._uow.user_repository.get_user_by_email(new_email):
                raise EmailAlreadyExist()
            user.email = new_email
            updated_user = await self._uow.user_repository.update_user(user_id,user)
            return UserDTO.model_validate(updated_user) 

    async def change_user_password(self, user_id: UUID4, new_password: str) -> UserDTO | None:
        """The method changing user password.
        
        Args:
            user_id (UUID4): The user id.
            new password (str): The new user password.

        Returns:
            UserDTO | None: The updated user record.
        """
        async with self._uow:
            user = await self._uow.user_repository.get_user_by_uuid(user_id=user_id)
            if not user:
                return None
            user.password = hash_password(new_password)
            updated_user = await self._uow.user_repository.update_user(user_id,user)
            return UserDTO.model_validate(updated_user) 

    async def set_role(self, user_id: UUID4, role: UserRole) -> UserDTO | None:
        """The abstarct setting role for the user.
        
        Args:
            user_id (UUID4): The user id.
            role (UserRole): the role to set.
            
        Returns:
            UserDTO | None: The updated user record.
        """
        async with self._uow:
            user = await self._uow.user_repository.get_user_by_uuid(user_id=user_id)
            if not user:
                return None
            user.role = role
            updated_user = await self._uow.user_repository.update_user(user_id, user)
            return UserDTO.model_validate(updated_user) if updated_user else None

    async def authenticate_user(self, user: UserLogin) -> TokenDTO | None:
        """The method authenticating the user.

        Args:
            user (UserLogin): The user data.

        Returns:
            TokenDTO | None: The token details.
        """
        async with self._uow:
            if user_data := await self._uow.user_repository.get_user_by_email(user.email):
                if verify_password(user.password, user_data.password):
                    token_details = generate_user_token(user_data.user_id)
                    # trunk-ignore(bandit/B106)
                    return TokenDTO(**token_details)

                return None

            return None

    async def create_admin_if_not_exists(self):
        """Creates a default admin/librarian user if one does not already exist."""
        async with self._uow:
            existing = await self._uow.user_repository.get_user_by_email("admin@example.com")
            if existing:
                return
            admin = UserCreate(
                username="admin",
                email="admin@example.com",
                password="haslo",
            )
            user = await self._uow.user_repository.add_user(admin)
            user.role = UserRole.librarian
            await self._uow.user_repository.update_user(user.user_id, user)
        
