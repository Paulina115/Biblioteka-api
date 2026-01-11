"""Module containing unit of work implementation"""

from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.repositories.book import BookRepository
from src.infrastructure.repositories.book_copy import BookCopyRepository
from src.infrastructure.repositories.history import HistoryRepository
from src.infrastructure.repositories.reservation import ReservationRepository
from src.infrastructure.repositories.user import UserRepository
from src.infrastructure.services.iunit_of_work import IUnitOfWork
from src.db import async_session_factory


class UnitOfWork(IUnitOfWork):
    """Class implementing unit of work."""
    def __init__(self, async_session_factory = async_session_factory):
        self._async_session_factory = async_session_factory
   
    async def __aenter__(self):
        self._session: AsyncSession = self._async_session_factory()

        self.book_repository = BookRepository(self._session)
        self.copy_repository = BookCopyRepository(self._session)
        self.history_repository = HistoryRepository(self._session)
        self.reservation_repository = ReservationRepository(self._session)
        self.user_repository = UserRepository(self._session)
        
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        try:
            if exc_value:
                await self._session.rollback()
            else:
                await self._session.commit()
        finally:
            await self._session.close()


    async def commit(self):
       await self._session.commit()

    async def rollback(self):
        await self._session.rollback()
