# from typing import Iterable

# from dependency_injector.wiring import inject, Provide
# from fastapi import APIRouter, Depends, HTTPException

# from src.container import Container
# from src.infrastructure.services.ihistory import IHistoryService
# from src.infrastructure.dto.historydto import HistoryDTO
# from src.core.domain.history import History

# router = APIRouter()

# @router.get("/all", response_model=Iterable[HistoryDTO])
# @inject
# async def get_all_history(
#     service: IHistoryService = Depends(Provide[Container.history_service]),
# ):
#     history = await service.get_all_history()
#     return history


# @router.get("/{user_id}", response_model=HistoryDTO)
# @inject
# async def get_history_by_user(
#     user_id: int,
#     service: IHistoryService = Depends(Provide[Container.history_service]),
# ):
#     history = await service.get_history_by_user(user_id)
#     if not history:
#         raise HTTPException(status_code=404)
#     return history

# @router.get("/{book_id}", response_model=HistoryDTO)
# @inject
# async def get_history_by_book(
#     book_id: int,
#     service: IHistoryService = Depends(Provide[Container.history_service]),
# ):
#     history = await service.get_history_by_book(book_id)
#     if not history:
#         raise HTTPException(status_code=404)
#     return history

# @router.put("/{history_id}", response_model=HistoryDTO)
# @inject
# async def update_history(
#     history_id: int,
#     data: History,
#     service: IHistoryService = Depends(Provide[Container.history_service]),
# ):
#     updated = await service.update_history(history_id, data)
#     if not updated:
#         raise HTTPException(status_code=404)
#     return updated
