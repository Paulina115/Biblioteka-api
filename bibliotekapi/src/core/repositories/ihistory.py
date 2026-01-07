"""Module containing history repository implementation"""

from abc import ABC, abstractmethod
from uuid import UUID

from src.core.domain.history import HistoryCreate, History, HistoryStatus


class IHistoryRepository(ABC):
    """An abstract class representing protocol of history repository."""

    @abstractmethod
    async def get_all_history(self, status: HistoryStatus | None = None) -> list[History]:
        """The abstract getting a all history from the data storage.
            Optionally filter by status
        
        Args:
            status (HistoryStatus | None): History status.
        
        Returns:
            list[History]: The collection of all history data.
        """

    @abstractmethod
    async def get_history_by_id(self, history_id: int) -> History | None:
        """The abstract getting a single history record from the data storage.
        
        Args:
            history_id (int): The id of the history.

        Returns:
            History | None: The history data if exists.
        """

    @abstractmethod
    async def get_history_by_user(self, user_id: UUID, status: HistoryStatus | None = None) -> list[History]:
       """The abstract getting a history for a given user from the data storage.
            Optionally filter by status.
        Args:
            user_id (UUID): The id of the user.
            status (HistoryStatus): The history status.

        Returns:
            List[History]: The collection of history data for a given user.
        """
    
    @abstractmethod
    async def get_history_by_user_and_copy(self, user_id: UUID, copy_id: int) -> History:
       """The abstract getting a history for a given user and book copy from the data storage.
        Args:
            user_id (UUID): The id of the user.
            copy_id (int): The book copy id.

        Returns:
            History: The history data for a given user and book copy if exist.
        """

    @abstractmethod
    async def add_history(self, data: HistoryCreate) -> History | None:
        """The abstract adding new history record to the data storage.
        
        Args:
            data (HistoryCreate): The attributes of the history.

        Returns:
            History | None: The newly created history record.
        """

    @abstractmethod
    async def update_history(self, history_id: int, data: HistoryCreate) -> History | None:
        """The abstarct updating history data in the data storage.
        
        Args:
            history_id (int): The history id.
            data (HistoryCreate): The attributes of the history record.

        Returns:
            History | None: The updated history record.
        """

    @abstractmethod
    async def delete_history(self, history_id: int) -> bool:
       """The abstarct removing a single history record from the data storage.

        Args:
            history_id (int): The history id.

        Returns:
            bool: Success of the operation.
        """
    @abstractmethod
    async def delete_history_by_user(self, user_id: int) -> bool:
       """The abstarct removing all history records for a user from the data storage.

        Args:
            user_id (int): The user id.

        Returns:
            bool: Success of the operation.
        """
