"""Module containing user repository implementation"""


from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import UUID4

from src.infrastructure.utils.password import hash_password
from src.core.repositories.iuser import IUserRepository
from src.core.domain.user import User as UserDomain, UserCreate

from src.db import User as UserORM

class UserRepository(IUserRepository):
    """A class implementing the user repository"""

    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_all_users(self) -> list[UserDomain]:
       """The method getting all users from the data storage.
        
        Returns:
            list[UserDomain]: The collection of the all users.
        """
       stmt = select(UserORM)
       users = (await self._session.scalars(stmt)).all()
       return [UserDomain.model_validate(user) for user in users]
       

    async def get_user_by_uuid(self, user_id: UUID4) -> UserDomain | None:
        """The method getting a user from the data storage.

        Args:
            user_id (UUID4): The id of the user.
        
        Returns:
            UserDomain | None: The user data if exists.
        """
        user = await self._get_user_by_uuid(user_id)
        if user:
            return UserDomain.model_validate(user)
        return None

    async def get_user_by_email(self, email: str) -> UserDomain | None:
        """The method getting a user by email from the data storage.

        Args:
            email (str): The email of the user.
        
        Returns:
            UserDomain | None: The user data if exists.
        """
        stmt = select(UserORM).where(UserORM.email==email)
        user = (await self._session.scalars(stmt)).first()
        return UserDomain.model_validate(user) if user else None

    async def get_user_by_username(self, username: str) -> list[UserDomain]:
        """The method getting a user by username from the data storage.

        Args:
            username (str): The username of the user.
        
        Returns:
            list[UserDomain]: The collection of users data.
        """
        stmt = select(UserORM).where(UserORM.username==username)
        users = (await self._session.scalars(stmt)).all()
        return [UserDomain.model_validate(user) for user in users]
        
    async def add_user(self, data: UserCreate) -> UserDomain | None:
        """The method adding new user to the data storage.
        
        Args:
            data (UserCreate): The attributes of the user.
        Returns:
            UserDomain | None: The newly created user.
        """
        new_user = UserORM(
        **data.model_dump(exclude={"password"}),
        password=hash_password(data.password),
        )

        self._session.add(new_user)
        await self._session.flush()
        return UserDomain.model_validate(new_user) if new_user else None


    async def update_user(self, user_id: UUID4, data: UserDomain) -> UserDomain | None:
        """The method updating user data in the data storage.
        
        Args:
            user_id (UUID4): The user id.
            data (UserDomain): The attributes of the user.

        Returns:
            UserDomain | None: The updated user.
        """
        user = await self._get_user_by_uuid(user_id)
        if user:
            for field, value in data.model_dump().items():
                setattr(user, field, value)
            await self._session.flush()
            return UserDomain.model_validate(user)
        return None

    async def delete_user(self, user_id: UUID4) -> bool:
        """The method removing user from the data storage.

        Args:
            user_id (UUID4): The user id.

        Returns:
            bool: Success of the operation.
        """
        user = await self._get_user_by_uuid(user_id)
        if user:
            await self._session.delete(user)
            await self._session.flush()
            return True
        return False
    
    async def _get_user_by_uuid(self, user_id: UUID4) -> UserORM | None:
        """A private method getting user from the DB based on its UUID.

        Args:
            user_id (UUID4): The ID of the user.

        Returns:
            USerORM | None: the user data if exists.
        """
        stmt = select(UserORM).where(UserORM.user_id == user_id)
        user = (await self._session.scalars(stmt)).first()
        return  user if user else None

    