"""Module containing history repository implementation"""

from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from src.core.repositories.ihistory import IHistoryRepository
from src.core.domain.history import History as HistoryDomain, HistoryCreate, HistoryStatus
from src.db import History as HistoryORM, async_session_factory

class HistoryRepository(IHistoryRepository):
    """A class implementing the history repository"""
    
    def __init__(self, sessionmaker = async_session_factory):
        self._sessionmaker = sessionmaker
        
    async def get_all_history(self, status: HistoryStatus | None = None) -> list[HistoryDomain]:
        """The method getting a all history from the data storage.
        
        Returns:
            list[HistoryDomain]: The collection of all history data.
        """
        async with self._sessionmaker() as session:
            stmt = select(HistoryORM)
            if status is not None:
                stmt = stmt.where(HistoryORM.status==status)
            history = (await session.scalars(stmt)).all()
            return [HistoryDomain.model_validate(h) for h in history]



    async def get_history_by_id(self, history_id: int) -> HistoryDomain | None:
        """The method getting a single history record from the data storage.
        
        Args:
            history_id (int): The id of the history.

        Returns:
            HistoryDomain | None: The history data if exists.
        """
        async with self._sessionmaker() as session:
            history = await self._get_by_id(history_id, session)
            return HistoryDomain.model_validate(history) if history else None

    async def get_history_by_user(self, user_id: UUID, status: HistoryStatus | None = None) -> list[HistoryDomain]:
       """The method getting a history for a given user from the data storage.
            Optionally filter by status.
        
        Args:
            user_id (UUID): The id of the user.
            status (History status): The history status.

        Returns:
            List[HistoryDomain]: The collection of history data for a given user.
        """
       async with self._sessionmaker() as session:
           stmt = select(HistoryORM).where(HistoryORM.user_id == user_id)
           if status is not None:
                stmt = stmt.where(HistoryORM.status==status)
           history = (await session.scalars(stmt)).all()
           return [HistoryDomain.model_validate(h) for h in history]

    async def get_history_by_user_and_copy(self, user_id: UUID, copy_id: int) -> HistoryDomain | None:
       """The method getting a history for a given user and book copy from the data storage.
        Args:
            user_id (UUID): The id of the user.
            copy_id (int): The id of the book copy.

        Returns:
            HistoryDomain: The history data for a given user and book copy if exist.
        """
       async with self._sessionmaker() as session:
           stmt = ( select(HistoryORM)
                   .where(HistoryORM.user_id == user_id,
                          HistoryORM.copy_id ==  copy_id)
           )
           history = (await session.scalars(stmt)).first()
           return HistoryDomain.model_validate(history) if history else None

    async def add_history(self, data: HistoryCreate) -> HistoryDomain | None:
        """The method adding new history record to the data storage.
        
        Args:
            data (HistoryCreate): The attributes of the history.

        Returns:
            HistoryDomain | None: The newly created history record.
        """
        async with self._sessionmaker() as session:
            new_history = HistoryORM(**data.model_dump())
            session.add(new_history)
            await session.commit()
            return HistoryDomain.model_validate(new_history) if new_history else None

    async def update_history(self, history_id: int, data: HistoryCreate) -> HistoryDomain | None:
        """The method updating history data in the data storage.
        
        Args:
            history_id (int): The history id.
            data (HistoryCreate): The attributes of the history record.

        Returns:
            HistoryDomain | None: The updated history record.
        """
        async with self._sessionmaker() as session:
            history = await self._get_by_id(history_id, session)
            if history:
                for field, value in data.model_dump().items():
                    setattr(history, field, value)
                await session.commit()
                return HistoryDomain.model_validate(history)
            return None

    async def delete_history(self, history_id: int) -> bool:
       """The method removing a single history record from the data storage.

        Args:
            history_id (int): The history id.

        Returns:
            bool: Success of the operation.
        """
       async with self._sessionmaker() as session:
           history = await self._get_by_id(history_id, session)
           if history:
               await session.delete(history)
               await session.commit()
               return True
           return False
       
    async def delete_history_by_user(self, user_id: UUID) -> bool:
       """The method removing all history records for a user from the data storage.

        Args:
            user_id (UUID): The user id.

        Returns:
            bool: Success of the operation.
        """
       async with self._sessionmaker() as session:
           stmt = delete(HistoryORM).where(HistoryORM.user_id==user_id)
           result = await session.execute(stmt)
           await session.commit()
           return result.rowcount > 0
                    
       
    async def _get_by_id(self, history_id: int, session: AsyncSession) -> HistoryORM | None:
        """A private method getting history record from the DB based on its ID.

        Args:
            history_id (int): The ID of the history.
            session (AsyncSession): session for query.

        Returns:
            HistoryORM | None: History record if exists.
        """
        return await session.get(HistoryORM, history_id)
        
    