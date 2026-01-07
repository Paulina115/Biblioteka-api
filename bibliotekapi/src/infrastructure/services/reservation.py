"""Module containing reservation service implementation"""

from datetime import datetime, timedelta

from src.infrastructure.dto.reservationdto import ReservationDTO
from src.infrastructure.dto.historydto import HistoryDTO
from src.core.domain.reservation import ReservationStatus
from src.core.domain.history import HistoryStatus
from src.core.domain.book_copy import BookCopy, BookCopyStatus
from src.core.repositories.ireservation import IReservationRepository
from src.core.repositories.ibook_copy import IBookCopyRepository
from src.core.repositories.ihistory import IHistoryRepository
from src.infrastructure.services.ireservation import IReservationService

class ReservationService(IReservationService):
    """Class implementing reservation service."""

    _repository: IReservationRepository
    _copy_repository: IBookCopyRepository
    _history_repository: IHistoryRepository

    def __init__(self, repository: IReservationRepository, copy_repository: IBookCopyRepository, history_repository: IHistoryRepository):
        self._repository = repository
        self._copy_repository = copy_repository
        self._history_repository = history_repository
     
    async def get_all_reservations(self, status: ReservationStatus | None = None) -> list[ReservationDTO]:
        """The method getting a all reservations from the repository (Intended for Librarian use).
            Optionally filter by status.

        Args:
            status (ReservationStatus | None): status of reservation.
        
        Returns:
            list[ReservationDTO]: The collection of reservations data.
        """
        reservations = await self._repository.get_all_reservations()
        return [ReservationDTO.model_validate(reservation) for reservation in reservations]

    async def get_reservation_by_id(self, reservation_id: int) -> ReservationDTO | None:
        """The method getting a reservation record from the repository (Intended for Librarian use).
        
        Args:
            reservation_id (int): The id of the reservation.

        Returns:
            ReservationDTO | None: The reservation data if exists.
        """
        reservation = await self._repository.get_reservation_by_id(reservation_id)
        return ReservationDTO.model_validate(reservation) if reservation else None

    async def get_reservations_by_user(self, user_id: int, status: ReservationStatus | None = None) -> list[ReservationDTO]:
       """The method getting a reservations for a given user from the repository (Intended for Librarian use).
            Optionally filter by status.
        Args:
            user_id (int): The id of the user.
            status (ReservationStatus | None): status of reservation.
        
        Returns:
            List[ReservationDTO]: The collection of reservation data for a given user.
        """
       reservations = await self._repository.get_reservation_by_user(user_id, status)
       return [ReservationDTO.model_validate(reservation) for reservation in reservations]
       
    async def get_user_reservations(self, user_id: int, status: ReservationStatus | None = None) -> list[ReservationDTO]:
       """The method getting a reservations for currently authenticated user from the repository.
            Optionally filter by status.

        Args:
            user_id (int): The user_id.
            status (ReservationStatus | None): status of reservation.

        Returns:
            List[ReservationDTO]: The collection of reservation data for the user.
        """
       reservations = await self._repository.get_reservation_by_user(user_id, status)
       return [ReservationDTO.model_validate(reservation) for reservation in reservations]

    async def add_reservation(self, book_id: int, user_id: int ) -> ReservationDTO | None:
        """The method adding new reservation to the repository.
        
        Args:
            book_id (int): id of the reserving book.
            user_id (int): id of the user.
        Returns:
            ReservationDTO | None: The newly created reservation record.
        """

    async def cancel_reservation(self, reservation_id: int) -> ReservationDTO:
       """The method removing reservation from the repository.

        Args:
            reservation_id (int): The reservation id.

        Returns:
            ReservationDTO: Updated reservation record.
        """
       
    async def mark_as_collected(self, reservation_id: int) -> ReservationDTO:
       """The method changing  reservation status to collected.

        Args:
            reservation_id (int): The reservation id.

        Returns:
            ReservationDTO: Updated reservation record.
        """
       
    

