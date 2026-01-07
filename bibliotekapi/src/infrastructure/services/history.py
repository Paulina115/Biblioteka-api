"""Module containing history service implementation"""

from uuid import UUID
from datetime import datetime, timedelta

from src.infrastructure.dto.historydto import HistoryDTO
from src.core.domain.history import HistoryCreate, HistoryStatus
from src.core.domain.book_copy import BookCopyStatus
from src.core.repositories.ihistory import IHistoryRepository
from src.core.repositories.ibook_copy import IBookCopyRepository
from src.infrastructure.services.ihistory import IHistoryService

class HistoryService(IHistoryService):
    """A class implementing history service"""
    _repository: IHistoryRepository
    _copy_repository: IBookCopyRepository

    def __init__(self, repository: IHistoryRepository, copy_repository: IBookCopyRepository):
        self._repository = repository
        self._copy_repository = copy_repository
    
    async def get_all_history(self, status: HistoryStatus | None = None) -> list[HistoryDTO]:
        """The method getting all history from the repository (Intendend for Librarian use).
            Optionally filter by status.

        Args:
            status: HistoryStatus | None = None: status of a book in history record.
        Returns:
            list[HistoryDTO]: The collection of all history data.
        """
        history = await self._repository.get_all_history(status)
        return [HistoryDTO.model_validate(h) for h in history]

    async def get_history_by_user(self, user_id: UUID, status: HistoryStatus | None = None) -> list[HistoryDTO]:
       """The method getting a history for a given user from the repository (Intendend for Librarian use).
            Optionally filter by status.

        Args:
            user_id (UUID): The id of the user.
            status: HistoryStatus | None = None: status of a book in history record.

        Returns:
            list[HistoryDTO]: The collection of history data for a given user.
        """
       history = await self._repository.get_history_by_user(user_id, status)
       return [HistoryDTO.model_validate(h) for h in history]

    async def get_user_history(self, user_id: UUID, status: HistoryStatus | None = None) -> list[HistoryDTO]:
       """The method getting a borrowing history for the currently authenticated user.
          Optionally filter by status.

        Args:
            user_id (UUID): The id of the user.
            status: HistoryStatus | None = None: status of a book in history record.

        Returns:
            list[HistoryDTO]: The collection of history data for a given user.
        """
       history = await self._repository.get_history_by_user(user_id, status)
       return [HistoryDTO.model_validate(h) for h in history]

    async def mark_as_returned(self, user_id: UUID, copy_id: int) -> HistoryDTO | None:
       """The method changing borrowed book status to returned.

        Args:
            user_id (int): The user id.
            book_copy_id (int): The book copy id.

        Returns:
            HistoryDTO: Updated history data.
        """
       history = await self._repository.get_history_by_user_and_copy(user_id, copy_id)
       if not history:
            return None
       if history.status != HistoryStatus.borrowed:
            raise ValueError("This copy is not currently borrowed")

       history.status = HistoryStatus.returned
       history.return_date = datetime.now()
       copy = await self._copy_repository.get_book_copy_by_id(copy_id)
       copy.status = BookCopyStatus.available
       await self._copy_repository.update_book_copy(copy)
       return await self._repository.update_history(history.history_id, history)
       
       
    async def mark_as_borrowed(self, user_id: UUID, copy_id: int) -> HistoryDTO | None:
       """The method marking book as borrowed in history record.

        Args:
            user_id (UUID): The user id.
            book_copy_id (int): The book id.

        Returns:
            HistoryDTO: New history data.
        """
       history = await self._repository.get_history_by_user_and_copy(user_id, copy_id)
       if history:
            raise ValueError("This copy is already borrowed by the user")
       data = HistoryCreate(user_id=user_id,copy_id=copy_id)
       new_history = await self._repository.add_history(data)
       copy = await self._copy_repository.get_book_copy_by_id(copy_id)
       copy.status = BookCopyStatus.borrowed
       await self._copy_repository.update_book_copy(copy)
       return new_history
    
    async def prolong_borrowing_period(self, user_id: UUID, book_copy_id: int, period: int = 7 ) -> HistoryDTO | None:
       """The method extending the borrowing due date.

        Args:
            user_id (UUID): The user id.
            book_copy_id (int): The book copy id.
            period (int): Number of days to extend the borrowing period (default is 7).

        Returns:
            HistoryDTO: Updated history data.
        """
       history = await self._repository.get_history_by_user_and_copy(user_id, book_copy_id)
       if not history:
            return None
       if history.status != HistoryStatus.borrowed:
            raise ValueError("Cannot extend borrowing period for a returned book")

       history.due_date += timedelta(days=period)
       return await self._repository.update_history(history.history_id, history)
    