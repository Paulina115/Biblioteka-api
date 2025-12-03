from typing import Iterable
from datetime import datetime, timedelta

from src.core.domain.reservation import Reservation
from src.core.domain.history import History
from src.core.repositories.ireservation import IReservationRepository
from src.core.repositories.ibook import IBookRepository
from src.core.repositories.ihistory import IHistoryRepository
from src.infrastructure.services.ireservation import IReservationService

class ReservationService(IReservationService):

    _repository: IReservationRepository
    _book_repository: IBookRepository
    _history_repository: IHistoryRepository

    def __init__(self, repository: IReservationRepository, book_repository: IBookRepository, history_repository: IHistoryRepository):
        self._repository = repository
        self._book_repository = book_repository
        self._history_repository = history_repository
    
    async def get_all_reservations(self) -> Iterable[Reservation]:
       return await self._repository.get_all_reservations()

    async def get_reservation_by_id(self, id : int) -> Reservation:
        return await self._repository.get_reservation_by_id(id)
    
    async def get_reservations_by_user(self, user_id: int) -> Iterable[Reservation]:
       return await self._repository.get_reservations_by_user(user_id)
    
    async def get_reservation_by_book(self, book_id: int) -> Reservation:
        return await self._repository.get_reservation_by_book(book_id)
    
    async def add_reservation(self, data: Reservation) -> None:
        return await self._repository.add_reservation(data)

    async def update_reservation(self, id: int) -> None:
        return await self._repository.update_reservation(id)
    
    async def cancel_reservation(self, id: int) -> None:
        return await self._repository.cancel_reservation(id)

    async def reserve_book(self, user_id: int, book_id: int) -> None:
       book = await self._book_repository.get_book_by_id(book_id)

       if not book.available:
           raise Exception("Book is already reserved")
       reservation = Reservation(
           user_id=user_id,
           book_id=book_id,
           reservation_date=datetime.now(),
           expiration_date=datetime.now() - timedelta(days=7),
           status="reserved"
       )

       reserved = await self._repository.add_reservation(reservation)

       book.available = False
       await self._book_repository.update_book(book_id,book)

       history = History(
           user_id=user_id,
           book_id=book_id,
           borrowed_date=datetime.now(),
           due_date=datetime.now() - timedelta(days=7),
           status="reserved"
       )
       await self._history_repository.update_history(history.id,history)
       return reserved

    async def return_book(self, user_id: int, book_id: int) -> None:
        reservation = await self._repository.get_reservation_by_book(book_id)
        if not reservation or reservation.user_id != user_id:
            raise Exception("Reservation not found")
        reservation.status = "returned"
        await self._repository.update_reservation(reservation.id, reservation)

        book = await self._book_repository.get_book_by_id(book_id)
        book.available = True
        await self._book_repository.update_book(book_id,book)

        history = await self._history_repository.get_history_by_book(book_id)
        for h in history:
            if h.user_id == user_id and h.book_id == h.book_id and h.status != "returned":
                h.return_date = datetime.now()
                h.status = "returned"
                await self._history_repository.update_history(h.id, h)

        return reservation