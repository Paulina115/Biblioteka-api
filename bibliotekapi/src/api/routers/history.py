"""A module containing history routers"""

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException
from pydantic import UUID4

from src.container import Container
from src.infrastructure.services.ihistory import IHistoryService
from src.core.domain.history import HistoryCreate, HistoryStatus
from src.infrastructure.dto.historydto import HistoryDTO
from src.infrastructure.dto.userdto import UserDTO
from src.infrastructure.auth.auth import librarian_required, get_current_user


router = APIRouter()

@router.get("/all", response_model=list[HistoryDTO])
@inject
async def get_all_history(
    status: HistoryStatus | None = None,
    service: IHistoryService = Depends(Provide[Container.history_service]),
    current_user: UserDTO = Depends(librarian_required)
) -> list:
    """The endpoint for getting all history from the repository (Intendend for Librarian use).
        Optionally filter by status.

    Args:
        status: HistoryStatus | None = None: status of a book in history record.
        service (IHistoryService): The injected service dependency.
        current_user (UserDTO): The injected user authentication dependency.

    Returns:
        list: The collection of all history data.
    """
    history = await service.get_all_history(status)
    return history
    

@router.get("/userid/{user_id}", response_model=list[HistoryDTO])
@inject
async def get_history_by_user(
    user_id: UUID4,
    status: HistoryStatus | None = None,
    service: IHistoryService = Depends(Provide[Container.history_service]),
    current_user: UserDTO = Depends(librarian_required)
) -> list:
    """The endpoint for getting a history for a given user from the repository (Intendend for Librarian use).
        Optionally filter by status.

    Args:
        user_id (UUID4): The id of the user.
        status (HistoryStatus | None = None) status of a book in history record.
        service (IHistoryService): The injected service dependency.
        current_user (UserDTO): The injected user authentication dependency.

    Returns:
        list: The collection of history data for a given user.
    """
    history = await service.get_history_by_user(user_id, status)
    return history


@router.get("/me", response_model=list[HistoryDTO])
@inject
async def get_user_history(
    status: HistoryStatus | None = None,
    service: IHistoryService = Depends(Provide[Container.history_service]),
    current_user: UserDTO = Depends(get_current_user)
) -> list:
    """The endpoint for getting a borrowing history for the currently authenticated user.
        Optionally filter by status.

    Args:
        status: HistoryStatus | None = None: status of a book in history record.
        service (IHistoryService): The injected service dependency.
        current_user (UserDTO): The injected user authentication dependency.

    Returns:
        list: The collection of history data for a given user.
    """
    user_id = current_user.user_id
    history = await service.get_history_by_user(user_id, status)
    return history

@router.patch("/return/{history_id}", response_model=HistoryDTO)
@inject
async def mark_as_returned(
     history_id: int,
     service: IHistoryService = Depends(Provide[Container.history_service]),
     current_user: UserDTO = Depends(librarian_required)
) -> dict:
    """The endpoint for changing borrowed book status to returned. (Intendend for Librarian use).

    Args:
        history_id (int): The history id.
        service (IHistoryService): The injected service dependency.
        current_user (UserDTO): The injected user authentication dependency.

    Returns:
        dict: Updated history data.
    """
    history = await service.mark_as_returned(history_id)
    if history:
        return history.model_dump()
    raise HTTPException(status_code=404, detail="History not found")
    
@router.patch("/borrow/{user_id}/{copy_id}", response_model=HistoryDTO)
@inject
async def mark_as_borrowed(
    user_id: UUID4, 
    copy_id: int,
    service: IHistoryService = Depends(Provide[Container.history_service]),
    current_user: UserDTO = Depends(librarian_required)
) -> dict:
    """The endpoint for marking book as borrowed in history record. (Intendend for Librarian use).

    Args:
        user_id (UUID4): The user id.
        copy_id (int): The book id.
        service (IHistoryService): The injected service dependency.
        current_user (UserDTO): The injected user authentication dependency.

    Returns:
        dict: Updated history data.
    """
    history = await service.mark_as_borrowed(user_id, copy_id)
    if history:
        return history.model_dump()
    raise HTTPException(status_code=404, detail="History not found.")

@router.put("/prolong/{history_id}", response_model=HistoryDTO)
@inject
async def prolong_borrowing_period(
     history_id: int, 
     period: int = 7,
     service: IHistoryService = Depends(Provide[Container.history_service]),
     current_user: UserDTO = Depends(librarian_required) 
) -> dict:
    """The endpoint for extending the borrowing due date. (Intendend for Librarian use).

    Args:
        history_id (int): The history id.
        period (int): Number of days to extend the borrowing period (default is 7).
        service (IHistoryService): The injected service dependency.
        current_user (UserDTO): The injected user authentication dependency.

    Returns:
        dict: Updated history data.
    """
    history = await service.prolong_borrowing_period(history_id, period)
    if history:
        return history.model_dump()
    raise HTTPException(status_code=404, detail="History not found.")


