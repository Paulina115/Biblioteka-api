"""Module containing unit of work abstractions"""

from abc import ABC, abstractmethod

from src.core.repositories.ibook import IBookRepository
from src.core.repositories.ibook_copy import IBookCopyRepository
from src.core.repositories.ihistory import IHistoryRepository
from src.core.repositories.ireservation import IReservationRepository
from src.core.repositories.iuser import IUserRepository

class IUnitOfWork(ABC):
    """An abstract unit of work class """
    book_repository: IBookRepository
    copy_repository: IBookCopyRepository
    history_repository: IHistoryRepository
    reservation_repository: IReservationRepository
    user_repository: IUserRepository

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        if exc_value:
            await self.rollback()
        else:
            await self.commit()


    @abstractmethod
    async def commit(self):
        pass

    @abstractmethod
    async def rollback(self):
        pass
