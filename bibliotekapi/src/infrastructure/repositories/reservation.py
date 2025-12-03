from typing import Any, Iterable

from asyncpg import Record  # type: ignore
from sqlalchemy import select

from core.repositories.ireservation import IReservationRepository
from core.domain.reservation import Reservation
from src.db import (
    reservation_table,
    user_table,
    database,
)
from src.infrastructure.dto.reservationdto import ReservationDTO



class ReservationRepository(IReservationRepository):

    async def get_all_reservations(self) -> Iterable[Reservation]:
        query = (
            select(reservation_table)
        )
        reservations = await database.fetch_all(query)

        return [ReservationDTO.from_record(Reservation) for reservation in reservations]
    
    async def get_reservation_by_id(self, id : int) -> Reservation | None:
        query = ( 
            select(reservation_table).where(reservation_table.id == id)
        )
        reservation = await database.fetch_one(query)
        
        return ReservationDTO.from_record(reservation ) if reservation else None

    async def get_reservations_by_user(self, user_id: int) -> Iterable[Reservation] | None:
        query = (
            select(reservation_table).where(reservation_table.user_id == user_id)
        )
        reservations = await database.fetch_all(query)

        return [ReservationDTO.from_record(reservation) for reservation in reservations]

    async def get_reservation_by_book(self, book_id: int) -> Reservation | None:
        query = (
            select(reservation_table).where(reservation_table.book_id == book_id)
        )
        reservation = await database.fetch_one(query)
        
        return ReservationDTO.from_record(reservation ) if reservation else None
    
    async def add_reservation(self, data: Reservation) -> None:
        query = (
            reservation_table.insert().values(**data.model_dump())
        )
        new_reservation_id = await database.execute(query)
        new_reservation = await self.get_reservation_by_id(new_reservation_id)

        return Reservation(**dict(new_reservation)) if new_reservation else None

    async def update_reservation(self, id: int,data: Reservation) -> None:
        if self._get_reservation_by_id(id):
            query = (
                reservation_table.update()
                .where(reservation_table.c.id == id)
                .values(**data.model_dump())
            )
            await database.execute(query)
        
            reservation = await self.get_reservation_by_id(id)

            return Reservation(**dict(reservation)) if reservation else None
        return None



    async def cancel_reservation(self, id: int) -> None:
        if self._get_reservation_by_id(id):
            query = ( reservation_table
            .delete()
            .where(reservation_table.c.id == id)
            )
            await database.execute(query)

            return True 
        return False
    

    async def _get_reservation_by_id(self, id: int) -> Record | None:
        query = (
            reservation_table.select()
            .where(reservation_table.c.id == id)
        )

        return await database.fetch_one(query)
