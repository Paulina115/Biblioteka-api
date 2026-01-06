"""Module containing reservation service abstractions"""

from abc import ABC, abstractmethod

from src.core.domain.reservation import Reservation, ReservationStatus


class IReservationService(ABC):

    """An abstract class representing protocol of reservation ."""

    @abstractmethod
    async def get_all_reservations(self, status: ReservationStatus | None = None) -> list[Reservation]:
        """The abstract getting a all reservations from the repository (Intended for Librarian use).
            Optionally filter by status.

        Args:
            status (ReservationStatus | None): status of reservation.
        
        Returns:
            list[Reservation]: The collection of reservations data.
        """

    @abstractmethod
    async def get_reservation_by_id(self, reservation_id: int) -> Reservation | None:
        """The abstract getting a reservation record from the repository (Intended for Librarian use).
        
        Args:
            reservation_id (int): The id of the reservation.

        Returns:
            Reservation | None: The reservation data if exists.
        """

    @abstractmethod
    async def get_reservations_by_user(self, user_id: int, status: ReservationStatus | None = None) -> list[Reservation]:
       """The abstract getting a reservations for a given user from the repository (Intended for Librarian use).
            Optionally filter by status.
        Args:
            user_id (int): The id of the user.
            status (ReservationStatus | None): status of reservation.
        
        Returns:
            List[Reservation]: The collection of reservation data for a given user.
        """
       
    @abstractmethod
    async def get_user_reservations(self, status: ReservationStatus | None = None) -> list[Reservation]:
       """The abstract getting a reservations for currently authenticated user from the repository.
            Optionally filter by status.

        Args:
            status (ReservationStatus | None): status of reservation.

        Returns:
            List[Reservation]: The collection of reservation data for the user.
        """

    @abstractmethod
    async def add_reservation(self, book_id: int, user_id: int ) -> Reservation | None:
        """The abstract adding new reservation to the repository.
        
        Args:
            book_id (int): id of the reserving book.
            user_id (int): id of the user.
        Returns:
            Reservation | None: The newly created reservation record.
        """

    @abstractmethod
    async def cancel_reservation(self, reservation_id: int) -> bool:
       """The abstarct removing reservation from the repository.

        Args:
            reservation_id (int): The reservation id.

        Returns:
            bool: Success of the operation.
        """

       
    

