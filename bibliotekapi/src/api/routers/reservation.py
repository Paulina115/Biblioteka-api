"""A module containing reservation routers"""

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException
from pydantic import UUID4

from src.container import Container
from src.infrastructure.services.ireservation import IReservationService
from src.core.domain.reservation import ReservationCreate, ReservationStatus
from src.infrastructure.dto.reservationdto import ReservationDTO
from src.infrastructure.dto.userdto import UserDTO
from src.infrastructure.auth.auth import librarian_required, get_current_user


router = APIRouter()

@router.get("/all", response_model=list[ReservationDTO])
@inject
async def get_all_reservations(
    status: ReservationStatus | None = None,
    service: IReservationService = Depends(Provide[Container.reservation_service]),
    current_user: UserDTO = Depends(librarian_required)
) -> list:
    """The endpoint for getting a all reservations from the repository (Intended for Librarian use).
        Optionally filter by status.

    Args:
        status (ReservationStatus | None): status of reservation.
        service (IReservationService): The injected service dependency.
        current_user (UserDTO): The injected user authentication dependency.

    Returns:
        list: The collection of reservations data.
    """
    reservations = await service.get_all_reservations(status)
    return reservations

@router.get("/reservationid/{reservation_id}", response_model=ReservationDTO)
@inject
async def get_reservation_by_id(
    reservation_id: int,
    service: IReservationService = Depends(Provide[Container.reservation_service]),
    current_user: UserDTO = Depends(librarian_required)
) -> dict:
    """The endpoint for getting a reservation record from the repository (Intended for Librarian use).

    Args:
        reservation_id (int): The id of the reservation.
        service (IHistoryService): The injected service dependency.
        current_user (UserDTO): The injected user authentication dependency.

    Returns:
        dict: The reservation data if exists.
    """
    reservation = await service.get_reservation_by_id(reservation_id)
    if reservation:
        return reservation.model_dump()
    raise HTTPException(status_code=404, detail="Reservation not found")

@router.get("/userid/{user_id}", response_model=list[ReservationDTO])
@inject
async def get_reservations_by_user(
    user_id: UUID4, 
    status: ReservationStatus | None = None,
    service: IReservationService = Depends(Provide[Container.reservation_service]),
    current_user: UserDTO = Depends(librarian_required)
) -> list:
    """The endpoint for getting a reservations for a given user from the repository (Intended for Librarian use).
        Optionally filter by status.
    Args:
        user_id (UUID4): The id of the user.
        status (ReservationStatus | None): status of reservation.
        service (IHistoryService): The injected service dependency.
        current_user (UserDTO): The injected user authentication dependency.

    Returns:
        list: The collection of reservation data for a given user.
    """
    reservations = await service.get_reservations_by_user(user_id, status)
    return reservations

@router.get("/me", response_model=list[ReservationDTO])
@inject
async def get_user_reservations(
    status: ReservationStatus | None = None,
    service: IReservationService = Depends(Provide[Container.reservation_service]),
    current_user: UserDTO = Depends(get_current_user)
) -> list:
    """The endpoint for getting a reservations for currently authenticated user from the repository.
        Optionally filter by status.

    Args:
        status (ReservationStatus | None): status of reservation.
        service (IHistoryService): The injected service dependency.
        current_user (UserDTO): The injected user authentication dependency.

    Returns:
        list: The collection of reservation data for the user.
    """
    user_id = current_user.user_id
    reservations = await service.get_reservations_by_user(user_id, status)
    return reservations

@router.post("/create", response_model=ReservationDTO, status_code=201)
@inject
async def add_reservation(
    book_id: int, 
    service: IReservationService = Depends(Provide[Container.reservation_service]),
    current_user: UserDTO = Depends(get_current_user) 
) -> dict:
    """The endpoind for adding new reservation to the repository.

    Args:
        book_id (int): id of the reserving book.
        service (IHistoryService): The injected service dependency.
        current_user (UserDTO): The injected user authentication dependency.

    Returns:
        dict: The newly created reservation record.
    """
    user_id = current_user.user_id
    reservation = await service.add_reservation(book_id, user_id)
    if reservation:
        return reservation.model_dump()
    raise HTTPException(status_code=404, detail="Reservation not found")

@router.patch("/cancel", response_model=ReservationDTO)
@inject
async def cancel_reservation(
    reservation_id: int,
    service: IReservationService = Depends(Provide[Container.reservation_service]),
    current_user: UserDTO = Depends(librarian_required)
) -> dict:
    """The endpoint for removing reservation from the repository. (Intendend for Librarian use).

    Args:
        reservation_id (int): The reservation id.
        service (IHistoryService): The injected service dependency.
        current_user (UserDTO): The injected user authentication dependency.

    Returns:
        dict: Updated reservation record.
    """
    reservation = await service.cancel_reservation(reservation_id)
    if reservation:
        return reservation.model_dump()
    raise HTTPException(status_code=404, detail="Reservation not found")




    
