from abc import ABC, abstractmethod
from typing import Iterable

from src.core.domain.reservation import Reservation
from src.infrastructure.dto.reservationdto import ReservationDTO


class IReservationService(ABC):

    @abstractmethod
    async def get_all_reservations(self) -> Iterable[Reservation]:
        pass

    @abstractmethod
    async def get_reservation_by_id(self, id : int) -> Reservation:
        pass

    @abstractmethod
    async def get_reservations_by_user(self, user_id: int) -> Iterable[Reservation]:
        pass

    @abstractmethod
    async def get_reservation_by_book(self, book_id: int) -> Reservation:
        pass

    @abstractmethod
    async def add_reservation(self, data: Reservation) -> None:
        pass

    @abstractmethod
    async def update_reservation(self, id: int) -> None:
        pass

    @abstractmethod
    async def cancel_reservation(self, id: int) -> None:
        pass

    @abstractmethod
    async def reserve_book(self, user_id: int, book_id: int) -> Reservation:
        pass

    @abstractmethod
    async def return_book(self, user_id: int, book_id) -> Reservation:
        pass

