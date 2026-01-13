"""Module containing reservation service implementation"""

from datetime import datetime, timedelta
from pydantic import UUID4

from src.infrastructure.dto.reservationdto import ReservationDTO
from src.core.domain.reservation import ReservationStatus, ReservationCreate
from src.core.domain.history import HistoryStatus
from src.core.domain.book_copy import BookCopy, BookCopyStatus
from src.core.repositories.ireservation import IReservationRepository
from src.infrastructure.services.iunit_of_work import IUnitOfWork
from src.infrastructure.services.ireservation import IReservationService
from src.core.exceptions.exceptions import UserNotFound, BookNotFound, BookNotAvailable, CopyNotFound

class ReservationService(IReservationService):
    """Class implementing reservation service."""

    def __init__(self, uow: IUnitOfWork ):
        self._uow = uow
     
    async def get_all_reservations(self, status: ReservationStatus | None = None) -> list[ReservationDTO]:
        """The method getting a all reservations from the repository (Intended for Librarian use).
            Optionally filter by status.

        Args:
            status (ReservationStatus | None): status of reservation.
        
        Returns:
            list[ReservationDTO]: The collection of reservations data.
        """
        async with self._uow:
            reservations = await self._uow.reservation_repository.get_all_reservations()
            return [ReservationDTO.model_validate(reservation) for reservation in reservations]

    async def get_reservation_by_id(self, reservation_id: int) -> ReservationDTO | None:
        """The method getting a reservation record from the repository (Intended for Librarian use).
        
        Args:
            reservation_id (int): The id of the reservation.

        Returns:
            ReservationDTO | None: The reservation data if exists.
        """
        async with self._uow:
            reservation = await self._uow.reservation_repository.get_reservation_by_id(reservation_id)
            return ReservationDTO.model_validate(reservation) if reservation else None

    async def get_reservations_by_user(self, user_id: UUID4, status: ReservationStatus | None = None) -> list[ReservationDTO]:
       """The method getting a reservations for a given user from the repository (Intended for Librarian use).
            Optionally filter by status.
        Args:
            user_id (UUID4): The id of the user.
            status (ReservationStatus | None): status of reservation.
        
        Returns:
            List[ReservationDTO]: The collection of reservation data for a given user.
        """
       async with self._uow:
        reservations = await self._uow.reservation_repository.get_reservation_by_user(user_id, status)
        return [ReservationDTO.model_validate(reservation) for reservation in reservations]
       
    async def get_user_reservations(self, user_id: UUID4, status: ReservationStatus | None = None) -> list[ReservationDTO]:
       """The method getting a reservations for currently authenticated user from the repository.
            Optionally filter by status.

        Args:
            user_id (UUID4): The user_id.
            status (ReservationStatus | None): status of reservation.

        Returns:
            List[ReservationDTO]: The collection of reservation data for the user.
        """
       async with self._uow:
            reservations = await self._uow.reservation_repository.get_reservation_by_user(user_id, status)
            return [ReservationDTO.model_validate(reservation) for reservation in reservations]

    async def add_reservation(self, book_id: int, user_id: UUID4 ) -> ReservationDTO | None:
        """The method adding new reservation to the repository.
        
        Args:
            book_id (int): id of the reserving book.
            user_id (UUID4): id of the user.
        Returns:
            ReservationDTO | None: The newly created reservation record.
        """
        async with self._uow:
            user = await self._uow.user_repository.get_user_by_uuid(user_id=user_id)
            if not user:
                raise UserNotFound()
            book = await self._uow.book_repository.get_book_by_id(book_id=book_id)
            if not book:
                raise BookNotFound()
            copies = await self._uow.copy_repository.get_copies_by_book(book_id=book_id, status=BookCopyStatus.available)
            if len(copies) < 1:
                raise BookNotAvailable()
            copy = copies[0]
            copy.status = BookCopyStatus.reserved
            await self._uow.copy_repository.update_book_copy(copy.copy_id, copy)
            reservation = await self._uow.reservation_repository.add_reservation(ReservationCreate(user_id=user_id, copy_id=copy.copy_id))
            return ReservationDTO.model_validate(reservation) if reservation else None

    async def cancel_reservation(self, reservation_id: int) -> ReservationDTO | None:
       """The method for canceling reservation.

        Args:
            reservation_id (int): The reservation id.

        Returns:
            ReservationDTO | None: Updated reservation record.
        """
       async with self._uow:
           reservation = await self._uow.reservation_repository.get_reservation_by_id(reservation_id)
           if not reservation:
               return None
           reservation.status = ReservationStatus.canceled
           copy = await self._uow.copy_repository.get_book_copy_by_id(reservation.copy_id)
           if not copy:
               raise CopyNotFound()
           copy.status = BookCopyStatus.available
           await self._uow.copy_repository.update_book_copy(copy.copy_id, copy)
           updated_reservation = await self._uow.reservation_repository.update_reservation(reservation_id, reservation)
           return ReservationDTO.model_validate(updated_reservation) if updated_reservation else None    