"""Module containing history service abstractions"""

from abc import ABC, abstractmethod
from uuid import UUID

from src.core.domain.history import History, HistoryStatus


class IHistoryService(ABC):
    """An abstract class representing protocol of history service."""

    @abstractmethod
    async def get_all_history(self, status: HistoryStatus | None = None) -> list[History]:
        """The abstract getting a all history from the repository (Intendend for Librarian use).
            Optionally filter by status.

        Args:
            status: HistoryStatus | None = None: status of a book in history record.
        Returns:
            list[History]: The collection of all history data.
        """

    @abstractmethod
    async def get_history_by_user(self, user_id: UUID, status: HistoryStatus | None = None) -> list[History]:
       """The abstract getting a history for a given user from the repository (Intendend for Librarian use).
            Optionally filter by status.

        Args:
            user_id (UUID): The id of the user.
            status: HistoryStatus | None = None: status of a book in history record.

        Returns:
            list[History]: The collection of history data for a given user.
        """

    @abstractmethod
    async def get_user_history(self, user_id: UUID, status: HistoryStatus | None = None) -> list[History]:
       """The abstract getting a borrowing history for the currently authenticated user.
          Optionally filter by status.

        Args:
            user_id (UUID): The id of the user.
            status: HistoryStatus | None = None: status of a book in history record.

        Returns:
            list[History]: The collection of history data for a given user.
        """
       
    @abstractmethod
    async def mark_as_returned(self, user_id: int, book_copy_id: int) -> History | None:
       """The abstarct changing borrowed book status to returned.

        Args:
            user_id (int): The user id.
            book_copy_id (int): The book copy id.

        Returns:
            History: Updated history data.
        """
       
    @abstractmethod
    async def mark_as_borrowed(self, user_id: int, book_copy_id: int) -> History | None:
       """The abstarct marking book as borrowed in history record.

        Args:
            user_id (int): The user id.
            book_copy_id (int): The book id.

        Returns:
            History: Updated history data.
        """
       
    @abstractmethod
    async def prolong_borrowing_period(self, user_id: int, book_copy_id: int, period: int = 7 ) -> History | None:
       """The abstarct extending the borrowing due date.

        Args:
            user_id (int): The user id.
            book_copy_id (int): The book copy id.
            period (int): Number of days to extend the borrowing period (default is 7).

        Returns:
            History: Updated history data.
        """
    