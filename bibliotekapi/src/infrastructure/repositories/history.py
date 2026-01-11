"""Module containing history repository implementation"""

from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import UUID4

from src.core.repositories.ihistory import IHistoryRepository
from src.core.domain.history import History as HistoryDomain, HistoryCreate, HistoryStatus
from src.db import History as HistoryORM

class HistoryRepository(IHistoryRepository):
    """A class implementing the history repository"""
    
    def __init__(self, session: AsyncSession):
        self._session = session
        
    async def get_all_history(self, status: HistoryStatus | None = None) -> list[HistoryDomain]:
        """The method getting a all history from the data storage.
        
        Returns:
            list[HistoryDomain]: The collection of all history data.
        """
        stmt = select(HistoryORM)
        if status is not None:
            stmt = stmt.where(HistoryORM.status==status)
        history = (await self._session.scalars(stmt)).all()
        return [HistoryDomain.model_validate(h) for h in history]



    async def get_history_by_id(self, history_id: int) -> HistoryDomain | None:
        """The method getting a single history record from the data storage.
        
        Args:
            history_id (int): The id of the history.

        Returns:
            HistoryDomain | None: The history data if exists.
        """
        history = await self._get_by_id(history_id)
        return HistoryDomain.model_validate(history) if history else None

    async def get_history_by_user(self, user_id: UUID4, status: HistoryStatus | None = None) -> list[HistoryDomain]:
       """The method getting a history for a given user from the data storage.
            Optionally filter by status.
        
        Args:
            user_id (UUID4): The id of the user.
            status (History status): The history status.

        Returns:
            List[HistoryDomain]: The collection of history data for a given user.
        """
       stmt = select(HistoryORM).where(HistoryORM.user_id == user_id)
       if status is not None:
            stmt = stmt.where(HistoryORM.status==status)
       history = (await self._session.scalars(stmt)).all()
       return [HistoryDomain.model_validate(h) for h in history]

    async def get_history_by_user_and_copy(self, user_id: UUID4, copy_id: int) -> HistoryDomain | None:
       """The method getting a history for a given user and book copy from the data storage.
        Args:
            user_id (UUID4): The id of the user.
            copy_id (int): The id of the book copy.

        Returns:
            HistoryDomain: The history data for a given user and book copy if exist.
        """
       stmt = ( select(HistoryORM)
                .where(HistoryORM.user_id == user_id,
                        HistoryORM.copy_id ==  copy_id)
        )
       history = (await self._session.scalars(stmt)).first()
       return HistoryDomain.model_validate(history) if history else None

    async def add_history(self, data: HistoryCreate) -> HistoryDomain | None:
        """The method adding new history record to the data storage.
        
        Args:
            data (HistoryCreate): The attributes of the history.

        Returns:
            HistoryDomain | None: The newly created history record.
        """
        new_history = HistoryORM(**data.model_dump())
        self._session.add(new_history)
        await self._session.flush()
        return HistoryDomain.model_validate(new_history) if new_history else None

    async def update_history(self, history_id: int, data: HistoryDomain) -> HistoryDomain | None:
        """The method updating history data in the data storage.
        
        Args:
            history_id (int): The history id.
            data (HistoryDomain): The attributes of the history record.

        Returns:
            HistoryDomain | None: The updated history record.
        """
        history = await self._get_by_id(history_id)
        if history:
            for field, value in data.model_dump().items():
                setattr(history, field, value)
            await self._session.flush()
            return HistoryDomain.model_validate(history)
        return None

    async def delete_history(self, history_id: int) -> bool:
       """The method removing a single history record from the data storage.

        Args:
            history_id (int): The history id.

        Returns:
            bool: Success of the operation.
        """
       history = await self._get_by_id(history_id)
       if history:
            await self._session.delete(history)
            await self._session.flush()
            return True
       return False
       
    async def delete_history_by_user(self, user_id: UUID4) -> bool:
       """The method removing all history records for a user from the data storage.

        Args:
            user_id (UUID4): The user id.

        Returns:
            bool: Success of the operation.
        """
       stmt = delete(HistoryORM).where(HistoryORM.user_id==user_id)
       result = await self._session.execute(stmt)
       await self._session.flush()
       return result.rowcount > 0
                    
       
    async def _get_by_id(self, history_id: int) -> HistoryORM | None:
        """A private method getting history record from the DB based on its ID.

        Args:
            history_id (int): The ID of the history.

        Returns:
            HistoryORM | None: History record if exists.
        """
        return await self._session.get(HistoryORM, history_id)
        
    