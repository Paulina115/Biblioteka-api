from typing import Any, Iterable

from sqlalchemy import select,join

from core.repositories.ireservation import IReservationRepository
from core.domain.reservation import Reservation


class ReservationRepository(IReservationRepository):

    async def get_all_reservations(self) -> Iterable[Reservation]:
        pass

    async def get_reservation_by_id(self, id : int) -> Reservation:
        pass

    async def get_reservations_by_user(self, user_id: int) -> Iterable[Reservation]:
        pass

    async def get_reservation_by_book(self, book_id: int) -> Reservation:
        pass

    async def add_reservation(self, data: Reservation) -> None:
        pass

    async def update_reservation(self, id: int) -> None:
        pass

    async def cancel_reservation(self, id: int) -> None:
        pass
