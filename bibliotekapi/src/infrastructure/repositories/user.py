"""Module containing user repository implementation"""


from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from src.infrastructure.utils.password import hash_password
from src.core.repositories.iuser import IUserRepository
from src.core.domain.user import User as UserDomain, UserCreate

from src.db import User as UserORM, async_session_factory

class UserRepository(IUserRepository):
    """A class implementing the user repository"""

    def __init__(self, sessionmaker = async_session_factory):
        self._sessionmaker = sessionmaker

    async def get_all_users(self) -> list[UserDomain]:
       """The method getting all users from the data storage.
        
        Returns:
            list[UserDomain]: The collection of the all users.
        """
       async with self._sessionmaker() as session:
           stmt = select(UserORM)
           users = (await session.scalars(stmt)).all()
           return [UserDomain.model_validate(user) for user in users]
       

    async def get_user_by_uuid(self, user_id: UUID) -> UserDomain | None:
        """The method getting a user from the data storage.

        Args:
            user_id (UUID4): The id of the user.
        
        Returns:
            UserDomain | None: The user data if exists.
        """
        async with self._sessionmaker() as session:
            user = await self._get_user_by_uuid(user_id, session)
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
        async with self._sessionmaker() as session:
            stmt = select(UserORM).where(UserORM.email==email)
            user = (await session.scalars(stmt)).first()
            return UserDomain.model_validate(user) if user else None

    async def get_user_by_username(self, username: str) -> list[UserDomain]:
        """The method getting a user by username from the data storage.

        Args:
            username (str): The username of the user.
        
        Returns:
            list[UserDomain]: The collection of users data.
        """
        async with self._sessionmaker() as session:
            stmt = select(UserORM).where(UserORM.username==username)
            users = (await session.scalars(stmt)).all()
            return [UserDomain.model_validate(user) for user in users]
        
    async def add_user(self, data: UserCreate) -> UserDomain | None:
        """The method adding new user to the data storage.
        
        Args:
            data (UserCreate): The attributes of the user.
        Returns:
            UserDomain | None: The newly created user.
        """
        async with self._sessionmaker() as session:
            new_user = UserORM(
            **data.model_dump(exclude={"password"}),
            password=hash_password(data.password),
        )

            session.add(new_user)
            await session.commit()
            return UserDomain.model_validate(new_user) if new_user else None


    async def update_user(self, user_id: UUID, data: UserCreate) -> UserDomain | None:
        """The method updating user data in the data storage.
        
        Args:
            user_id (UUID): The user id.
            data (UserCreate): The attributes of the user.

        Returns:
            UserDomain | None: The updated user.
        """
        async with self._sessionmaker() as session:
            user = await self._get_user_by_uuid(user_id, session)
            if user:
                for field, value in data.model_dump().items():
                    setattr(user, field, value)
                await session.commit()
                return UserDomain.model_validate(user)
            return None

    async def delete_user(self, user_id: UUID) -> bool:
        """The method removing user from the data storage.

        Args:
            user_id (UUID): The user id.

        Returns:
            bool: Success of the operation.
        """
        async with self._sessionmaker() as session:
            user = await self._get_user_by_uuid(user_id, session)
            if user:
                await session.delete(user)
                await session.commit()
                return True
            return False
    
    async def _get_user_by_uuid(self, user_id: UUID, session: AsyncSession) -> UserORM | None:
        """A private method getting user from the DB based on its UUID.

        Args:
            user_id (UUID): The ID of the user.
            session (AsyncSession): session for query.

        Returns:
            USerORM | None: the user data if exists.
        """
        stmt = select(UserORM).where(UserORM.user_id == user_id)
        user = (await session.scalars(stmt)).first()
        return  user if user else None

    