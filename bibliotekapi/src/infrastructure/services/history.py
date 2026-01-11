"""Module containing history service implementation"""

from pydantic import UUID4
from datetime import datetime, timedelta

from src.infrastructure.dto.historydto import HistoryDTO
from src.core.domain.history import HistoryCreate, HistoryStatus
from src.core.domain.book_copy import BookCopyStatus
from src.core.domain.reservation import ReservationStatus
from src.core.repositories.ihistory import IHistoryRepository
from src.infrastructure.services.iunit_of_work import IUnitOfWork
from src.infrastructure.services.ihistory import IHistoryService
from src.core.exceptions.exceptions import CopyNotFound, UserNotFound, CopyNotAvailable, BookNotBorrowed

class HistoryService(IHistoryService):
    """A class implementing history service"""
    _repository: IHistoryRepository

    def __init__(self, repository: IHistoryRepository, uow: IUnitOfWork ):
            self._repository = repository
            self._uow = uow

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

    async def get_history_by_user(self, user_id: UUID4, status: HistoryStatus | None = None) -> list[HistoryDTO]:
       """The method getting a history for a given user from the repository (Intendend for Librarian use).
            Optionally filter by status.

        Args:
            user_id (UUID4): The id of the user.
            status: HistoryStatus | None = None: status of a book in history record.

        Returns:
            list[HistoryDTO]: The collection of history data for a given user.
        """
       history = await self._repository.get_history_by_user(user_id, status)
       return [HistoryDTO.model_validate(h) for h in history]

    async def get_user_history(self, user_id: UUID4, status: HistoryStatus | None = None) -> list[HistoryDTO]:
       """The method getting a borrowing history for the currently authenticated user.
          Optionally filter by status.

        Args:
            user_id (UUID4): The id of the user.
            status: HistoryStatus | None = None: status of a book in history record.

        Returns:
            list[HistoryDTO]: The collection of history data for a given user.
        """
       history = await self._repository.get_history_by_user(user_id, status)
       return [HistoryDTO.model_validate(h) for h in history]

    async def mark_as_returned(self, history_id: int) -> HistoryDTO | None:
       """The method changing borrowed book status to returned (Intended for librarian).

        Args:
            history_id (int): The history record id.    
        
        Returns:
            HistoryDTO | None: Updated history data.
        """
       async with self._uow:
            history = await self._uow.history_repository.get_history_by_id(history_id)
            if not history:
                return None
            history.status = HistoryStatus.returned
            copy = await self._uow.copy_repository.get_book_copy_by_id(history.copy_id)
            if not copy:
                raise CopyNotFound()
            copy.status = BookCopyStatus.available
            await self._uow.copy_repository.update_book_copy(copy)
            new_history = await self._uow.history_repository.update_history(history)
            return HistoryDTO.model_validate(new_history)
            
    async def mark_as_borrowed(self, user_id: UUID4, copy_id: int) -> HistoryDTO | None:
       """The method marking book as borrowed in history record.

        Args:
            user_id (UUID4): The user id.
            copy_id (int): The book id.

        Returns:
            HistoryDTO | None: New history data.
        """
       async with self._uow:
            user = await self._uow.user_repository.get_user_by_uuid(user_id)
            if not user:
                raise UserNotFound()
            copy = await self._uow.copy_repository.get_book_copy_by_id(copy_id)
            if not copy:
                raise CopyNotFound()
            if copy.status != BookCopyStatus.available:
                raise CopyNotAvailable()
            history = await self._uow.history_repository.add_history(HistoryCreate(user_id=user_id, copy_id=copy_id))
            copy.status = BookCopyStatus.borrowed
            await self._uow.copy_repository.update_book_copy(copy)
            reservation = await self._uow.reservation_repository.get_reservation_by_user_and_copy(user_id, copy_id)
            if reservation:
                    reservation.status = ReservationStatus.collected
                    await self._uow.reservation_repository.update_reservation(reservation)
            return HistoryDTO.model_validate(history) if history else None
            
    async def prolong_borrowing_period(self, history_id: int, period: int = 7 ) -> HistoryDTO | None:
       """The method extending the borrowing due date.

        Args:
            history_id (int): The history id.
            period (int): Number of days to extend the borrowing period (default is 7).

        Returns:
            HistoryDTO | None: Updated history data.
        """
       async with self._uow:
            history = await self._uow.history_repository.get_history_by_id(history_id)
            if not history:
                return None
            if history.status != HistoryStatus.borrowed:
                raise BookNotBorrowed()
            history.due_date = history.due_date + timedelta(days=period)
            updated_history = await self._uow.history_repository.update_history(history)
            return HistoryDTO.model_validate(updated_history)
            