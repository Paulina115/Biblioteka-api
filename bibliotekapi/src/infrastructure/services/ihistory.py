"""Module containing history service abstractions"""

from abc import ABC, abstractmethod
from pydantic import UUID4

from src.infrastructure.dto.historydto import HistoryDTO
from src.core.domain.history import HistoryStatus


class IHistoryService(ABC):
    """An abstract class representing protocol of history service."""

    @abstractmethod
    async def get_all_history(self, status: HistoryStatus | None = None) -> list[HistoryDTO]:
        """The abstract getting a all history from the repository (Intendend for Librarian use).
            Optionally filter by status.

        Args:
            status: HistoryStatus | None = None: status of a book in history record.
        Returns:
            list[HistoryDTO]: The collection of all history data.
        """

    @abstractmethod
    async def get_history_by_user(self, user_id: UUID4, status: HistoryStatus | None = None) -> list[HistoryDTO]:
       """The abstract getting a history for a given user from the repository (Intendend for Librarian use).
            Optionally filter by status.

        Args:
            user_id (UUID4): The id of the user.
            status: HistoryStatus | None = None: status of a book in history record.

        Returns:
            list[HistoryDTO]: The collection of history data for a given user.
        """

    @abstractmethod
    async def get_user_history(self, user_id: UUID4, status: HistoryStatus | None = None) -> list[HistoryDTO]:
       """The abstract getting a borrowing history for the currently authenticated user.
          Optionally filter by status.

        Args:
            user_id (UUID4): The id of the user.
            status: HistoryStatus | None = None: status of a book in history record.

        Returns:
            list[HistoryDTO]: The collection of history data for a given user.
        """
       
    @abstractmethod
    async def mark_as_returned(self, history_id: int) -> HistoryDTO | None:
       """The abstarct changing borrowed book status to returned (Intended for librarian).

        Args:
            history_id (int): The history record id.

        Returns:
            HistoryDTO | None: Updated history data.
        """
       
    @abstractmethod
    async def mark_as_borrowed(self, user_id: UUID4, copy_id: int) -> HistoryDTO | None:
       """The abstarct marking book as borrowed in history record (Intended for librarian).

        Args:
            user_id (UUID4): The user id.
            copy_id (int): The book id.

        Returns:
            HistoryDTO | None: Updated history data.
        """
       
    @abstractmethod
    async def prolong_borrowing_period(self, history_id: int, period: int = 7 ) -> HistoryDTO | None:
       """The abstarct extending the borrowing due date (Intended for librarian).

        Args:
            history_id (int): The history record id.
            period (int): Number of days to extend the borrowing period (default is 7).

        Returns:
            HistoryDTO | None: Updated history data.
        """
    