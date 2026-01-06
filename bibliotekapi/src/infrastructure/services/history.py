"""Module containing history service implementation"""

from uuid import UUID

from src.core.domain.history import History, HistoryCreate, HistoryStatus
from src.core.repositories.ihistory import IHistoryRepository
from src.infrastructure.services.ihistory import IHistoryService

class HistoryService(IHistoryService):
    """A class implementing history service"""
    _repository: IHistoryRepository

    def __init__(self, repository: IHistoryRepository):
        self._repository = repository
    
    async def get_all_history(self, status: HistoryStatus | None = None) -> list[History]:
        """The method getting all history from the repository (Intendend for Librarian use).
            Optionally filter by status.

        Args:
            status: HistoryStatus | None = None: status of a book in history record.
        Returns:
            list[History]: The collection of all history data.
        """
        return await self._repository.get_all_history(status)

    async def get_history_by_user(self, user_id: UUID, status: HistoryStatus | None = None) -> list[History]:
       """The method getting a history for a given user from the repository (Intendend for Librarian use).
            Optionally filter by status.

        Args:
            user_id (UUID): The id of the user.
            status: HistoryStatus | None = None: status of a book in history record.

        Returns:
            list[History]: The collection of history data for a given user.
        """
       return await self._repository.get_history_by_user(user_id, status)

    async def get_user_history(self,user_id: UUID, status: HistoryStatus | None = None) -> list[History]:
       """The method getting a borrowing history for the currently authenticated user.
          Optionally filter by status.

        Args:
            user_id (UUID): The id of the user.
            status: HistoryStatus | None = None: status of a book in history record.

        Returns:
            list[History]: The collection of history data for a given user.
        """
       return await self._repository.get_history_by_user(user_id, status)
       
    async def mark_as_returned(self, user_id: UUID, book_copy_id: int) -> History | None:
       """The method changing borrowed book status to returned.

        Args:
            user_id (int): The user id.
            book_copy_id (int): The book copy id.

        Returns:
            History: Updated history data.
        """
       
       
    async def mark_as_borrowed(self, user_id: int, book_copy_id: int) -> History | None:
       """The method marking book as borrowed in history record.

        Args:
            user_id (int): The user id.
            book_copy_id (int): The book id.

        Returns:
            History: Updated history data.
        """
       
    async def prolong_borrowing_period(self, user_id: int, book_copy_id: int, period: int = 7 ) -> History | None:
       """The method extending the borrowing due date.

        Args:
            user_id (int): The user id.
            book_copy_id (int): The book copy id.
            period (int): Number of days to extend the borrowing period (default is 7).

        Returns:
            History: Updated history data.
        """
    