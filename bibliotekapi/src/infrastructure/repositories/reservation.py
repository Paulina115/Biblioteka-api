"""Module containing reservation repository implementation."""

from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import UUID4

from src.core.repositories.ireservation import IReservationRepository
from src.core.domain.reservation import Reservation as ReservationDomain, ReservationCreate, ReservationStatus
from src.db import Reservation as ReservationORM


class ReservationRepository(IReservationRepository):
    """A class implementing reservation repository."""

    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_all_reservations(self) -> list[ReservationDomain]:
        """The method getting a all reservations from the data storage.
        
        Returns:
            list[ReservationDomain]: The collection of reservations data.
        """
        stmt = select(ReservationORM)
        reservations = (await self._session.scalars(stmt)).all()
        return [ReservationDomain.model_validate(reservation) for reservation in reservations]


    async def get_reservation_by_id(self, reservation_id: int) -> ReservationDomain | None:
        """The method getting a reservation record from the data storage.
        
        Args:
            reservation_id (int): The id of the reservation.

        Returns:
            ReservationDomain | None: The reservation data if exists.
        """
        reservation = await self._get_reservation_by_id(reservation_id)
        if reservation:
            return ReservationDomain.model_validate(reservation)
        return None

    async def get_reservation_by_user(self, user_id: UUID4, status: ReservationStatus | None = None) -> list[ReservationDomain]:
       """The method getting a reservation for a given user from the data storage.
       Optionally filters by status. 
       
        Args:
            user_id (UUID4): The id of the user.
            status (ReservationStatus | None): The reservation status.

        Returns:
            List[ReservationDomain]: The collection of reservation data for a given user.
        """
       stmt = select(ReservationORM).where(ReservationORM.user_id==user_id)
       if status is not None:
            stmt = stmt.where(ReservationORM.status==status)
       reservations = (await self._session.scalars(stmt)).all()
       return [ReservationDomain.model_validate(reservation) for reservation in reservations]
       
    async def get_reservation_by_user_and_copy(self, user_id: UUID4, copy_id: int) -> ReservationDomain | None:
       """The method getting a reservation for a given user from the data storage.
       
        Args:
            user_id (UUID4): The id of the user.
            copy_id (int): The book copy id.

        Returns:
            ReservationDomain | None: The collection of reservation data for a given user.
        """
       stmt = select(ReservationORM).where(ReservationORM.user_id==user_id, ReservationORM.copy_id==copy_id)
       reservation = (await self._session.scalars(stmt)).first()
       if reservation:
            return ReservationDomain.model_validate(reservation)
       return None
    async def add_reservation(self, data: ReservationCreate) -> ReservationDomain | None:
        """The method adding new reservation to the data storage.
        
        Args:
            data (ReservationCreate): The attributes of the reservation.

        Returns:
            ReservationDomain | None: The newly created reservation record.
        """
        new_reservation = ReservationORM(**data.model_dump())
        self._session.add(new_reservation)
        await self._session.flush()
        return ReservationDomain.model_validate(new_reservation) if new_reservation else None

    async def update_reservation(self, reservation_id: int, data: ReservationDomain) -> ReservationDomain | None:
        """The method updating reservation in the data storage.
        
        Args:
            reservation_id (int): The reservation id.
            data (ReservationDomain): The attributes of the reservation.

        Returns:
            ReservationDomain | None: The updated reservation record.
        """
        reservation = await self._get_reservation_by_id(reservation_id)
        if reservation:
            for field, value in data.model_dump().items():
                setattr(reservation, field, value)
            await self._session.flush()
            return ReservationDomain.model_validate(reservation)
        return None

    async def delete_reservation(self, reservation_id: int) -> bool:
       """The method removing reservation from the data storage.

        Args:
            reservation_id (int): The reservation id.

        Returns:
            bool: Success of the operation.
        """
       reservation = await self._get_reservation_by_id(reservation_id)
       if reservation:
            await self._session.delete(reservation)
            await self._session.flush()
            return True
       return  False

    async def delete_reservation_by_user(self, user_id: UUID4) -> bool:
       """The method removing reservation for a user from the data storage.

        Args:
            user_id (UUID4): The user id.

        Returns:
            bool: Success of the operation.
        """
       stmt = delete(ReservationORM).where(ReservationORM.user_id==user_id)
       result = await self._session.execute(stmt)
       await self._session.flush()
       return result.rowcount > 0

    async def _get_reservation_by_id(self, reservation_id: int) -> ReservationORM | None:
        """A private method getting reservation from the DB based on its id.

        Args:
            reservation_id (UUID): The ID of the reservation.

        Returns:
            ReservationORM | None: the reservation data if exists.
        """
        stmt = select(ReservationORM).where(ReservationORM.reservation_id == reservation_id)
        reservation = (await self._session.scalars(stmt)).first()
        return  reservation if reservation else None
     
    