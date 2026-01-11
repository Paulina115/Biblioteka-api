"""Module containing reservation repository implementation"""

from abc import ABC, abstractmethod
from pydantic import UUID4

from src.core.domain.reservation import ReservationCreate, Reservation, ReservationStatus


class IReservationRepository(ABC):
    """An abstract class representing protocol of reservation repository."""

    @abstractmethod
    async def get_all_reservations(self) -> list[Reservation]:
        """The abstract getting a all reservations from the data storage.
        
        Returns:
            list[Reservation]: The collection of reservations data.
        """

    @abstractmethod
    async def get_reservation_by_id(self, reservation_id: int) -> Reservation | None:
        """The abstract getting a reservation record from the data storage.
        
        Args:
            reservation_id (int): The id of the reservation.

        Returns:
            Reservation | None: The reservation data if exists.
        """

    @abstractmethod
    async def get_reservation_by_user(self, user_id: UUID4, status: ReservationStatus | None = None) -> list[Reservation]:
       """The abstract getting a reservation for a given user from the data storage.
       Optionally filters by status.
        
        Args:
            user_id (UUID4): The id of the user.
            status (ResrvationStatus | None): The reservation status.

        Returns:
            List[Reservation]: The collection of reservation data for a given user.
        """
    
    @abstractmethod
    async def get_reservation_by_user_and_copy(self, user_id: UUID4, copy_id: int) -> Reservation | None:
       """The abstract getting a reservation for a given user from the data storage.
        
        Args:
            user_id (UUID4): The id of the user.
            copy_id (int): The book copy id.

        Returns:
            Reservation | None: The collection of reservation data for a given user.
        """

    @abstractmethod
    async def add_reservation(self, data: ReservationCreate) -> Reservation | None:
        """The abstract adding new reservation to the data storage.
        
        Args:
            data (ReservationCreate): The attributes of the reservation.

        Returns:
            Reservation | None: The newly created reservation record.
        """

    @abstractmethod
    async def update_reservation(self, reservation_id: int, data: Reservation) -> Reservation | None:
        """The abstarct updating reservation in the data storage.
        
        Args:
            reservation_id (int): The reservation id.
            data (Reservation): The attributes of the reservation.

        Returns:
            Reservation | None: The updated reservation record.
        """

    @abstractmethod
    async def delete_reservation(self, reservation_id: int) -> bool:
       """The abstarct removing reservation from the data storage.

        Args:
            reservation_id (int): The reservation id.

        Returns:
            bool: Success of the operation.
        """
    @abstractmethod
    async def delete_reservation_by_user(self, user_id: UUID4) -> bool:
       """The abstarct removing reservation for a user from the data storage.

        Args:
            user_id (UUID4): The user id.

        Returns:
            bool: Success of the operation.
        """




