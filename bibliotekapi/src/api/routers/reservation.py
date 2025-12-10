from typing import Iterable

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException

from src.container import Container
from src.infrastructure.services.ireservation import IReservationService
from src.infrastructure.dto.reservationdto import ReservationDTO
from src.core.domain.reservation import Reservation

router = APIRouter()

@router.get("/all", response_model=Iterable[ReservationDTO])
@inject
async def get_all_reservations(
    service: IReservationService = Depends(Provide[Container.reservation_service]),
):
    reservations = await service.get_all_reservations()
    return reservations

@router.get("/{reservation_id}", response_model=ReservationDTO)
@inject
async def get_reservation_by_id(
    reservation_id: int,
    service: IReservationService = Depends(Provide[Container.reservation_service]),
):
    reservation = await service.get_reservation_by_id(reservation_id)
    if not reservation:
        raise HTTPException(status_code=404)
    return reservation

@router.get("/{user_id}", response_model=ReservationDTO)
@inject
async def get_reservation_by_user(
    user_id: int,
    service: IReservationService = Depends(Provide[Container.reservation_service]),
):
    reservation = await service.get_reservation_by_user(user_id)
    if not reservation:
        raise HTTPException(status_code=404)
    return reservation

@router.get("/{book_id}", response_model=ReservationDTO)
@inject
async def get_reservation_by_book(
    book_id: int,
    service: IReservationService = Depends(Provide[Container.reservation_service]),
):
    reservation = await service.get_reservation_by_book(book_id)
    if not reservation:
        raise HTTPException(status_code=404)
    return reservation

@router.post("/", response_model=ReservationDTO, status_code=201)
@inject
async def add_reservation(
    data: Reservation,
    service: IReservationService = Depends(Provide[Container.reservation_service]),
):
    new_reservation = await service.add_reservation(data)
    return new_reservation


@router.put("/{reservation_id}", response_model=ReservationDTO)
@inject
async def update_reservation(
    reservation_id: int,
    data: Reservation,
    service: IReservationService = Depends(Provide[Container.reservation_service]),
):
    updated = await service.update_reservation(reservation_id, data)
    if not updated:
        raise HTTPException(status_code=404, detail="reservation not found")
    return updated


@router.delete("/{reservation_id}", status_code=204)
@inject
async def delete_reservation(
    reservation_id: int,
    service: IReservationService = Depends(Provide[Container.reservation_service]),
):
    result = await service.delete_reservation(reservation_id)
    if not result:
        raise HTTPException(status_code=404, detail="reservation not found")
    return None
