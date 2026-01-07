"""Module containing reservation repository implementation."""

from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from src.core.repositories.ireservation import IReservationRepository
from src.core.domain.reservation import Reservation as ReservationDomain, ReservationCreate, ReservationStatus
from src.db import Reservation as ReservationORM, async_session_factory




class ReservationRepository(IReservationRepository):
    """A class implementing reservation repository."""

    def __init__(self, sessionmaker = async_session_factory):
        self._sessionmaker = sessionmaker

    async def get_all_reservations(self) -> list[ReservationDomain]:
        """The method getting a all reservations from the data storage.
        
        Returns:
            list[ReservationDomain]: The collection of reservations data.
        """
        async with self._sessionmaker() as session:
            stmt = select(ReservationORM)
            reservations = (await session.scalars(stmt)).all()
            return [ReservationDomain.model_validate(reservation) for reservation in reservations]


    async def get_reservation_by_id(self, reservation_id: int) -> ReservationDomain | None:
        """The method getting a reservation record from the data storage.
        
        Args:
            reservation_id (int): The id of the reservation.

        Returns:
            ReservationDomain | None: The reservation data if exists.
        """
        async with self._sessionmaker() as session:
            reservation = await self._get_reservation_by_id(reservation_id, session)
            if reservation:
                return ReservationDomain.model_validate(reservation)
            return None

    async def get_reservation_by_user(self, user_id: UUID, status: ReservationStatus | None = None) -> list[ReservationDomain]:
       """The method getting a reservation for a given user from the data storage.
       Optionally filters by status. 
       
        Args:
            user_id (UUID): The id of the user.
            status (ReservationStatus | None): The reservation status.

        Returns:
            List[ReservationDomain]: The collection of reservation data for a given user.
        """
       async with self._sessionmaker() as session:
           stmt = select(ReservationORM).where(ReservationORM.user_id==user_id)
           if status is not None:
            stmt = stmt.where(ReservationORM.status==status)
           reservations = (await session.scalars(stmt)).all()
           return [ReservationDomain.model_validate(reservation) for reservation in reservations]

    async def add_reservation(self, data: ReservationCreate) -> ReservationDomain | None:
        """The method adding new reservation to the data storage.
        
        Args:
            data (ReservationCreate): The attributes of the reservation.

        Returns:
            ReservationDomain | None: The newly created reservation record.
        """
        async with self._sessionmaker() as session:
            new_reservation = ReservationORM(**data.model_dump())
            session.add(new_reservation)
            await session.commit
            return ReservationDomain.model_validate(new_reservation) if new_reservation else None

    async def update_reservation(self, reservation_id: int, data: ReservationCreate) -> ReservationDomain | None:
        """The method updating reservation in the data storage.
        
        Args:
            reservation_id (int): The reservation id.
            data (ReservationCreate): The attributes of the reservation.

        Returns:
            ReservationDomain | None: The updated reservation record.
        """
        async with self._sessionmaker() as session:
            reservation = await self._get_reservation_by_id(reservation_id, session)
            if reservation:
                for field, value in data.model_dump().items():
                    setattr(reservation, field, value)
                session.commit()
                return ReservationDomain.model_validate(reservation)
            return None

    async def delete_reservation(self, reservation_id: int) -> bool:
       """The method removing reservation from the data storage.

        Args:
            reservation_id (int): The reservation id.

        Returns:
            bool: Success of the operation.
        """
       async with self._sessionmaker() as session:
           reservation = await self._get_reservation_by_id(reservation_id, session)
           if reservation:
               await session.delete(reservation)
               await session.commit()
               return True
           return 
       False

    async def delete_reservation_by_user(self, user_id: UUID) -> bool:
       """The method removing reservation for a user from the data storage.

        Args:
            user_id (UUID): The user id.

        Returns:
            bool: Success of the operation.
        """
       async with self._sessionmaker() as session:
           stmt = delete(ReservationORM).where(ReservationORM.user_id==user_id)
           result = await session.execute(stmt)
           await session.commit()
           return result.rowcount > 0

    async def _get_reservation_by_id(self, reservation_id: int, session: AsyncSession) -> ReservationORM | None:
        """A private method getting reservation from the DB based on its id.

        Args:
            reservation_id (UUID): The ID of the reservation.
            session (AsyncSession): session for query.

        Returns:
            ReservationORM | None: the reservation data if exists.
        """
        stmt = select(ReservationORM).where(ReservationORM.reservation_id == reservation_id)
        reservation = (await session.scalars(stmt)).first()
        return  reservation if reservation else None
     
    