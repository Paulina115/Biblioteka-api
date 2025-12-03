from typing import Iterable

from src.core.domain.history import History
from src.core.repositories.ihistory import IHistoryRepository
from src.infrastructure.services.ihistory import IHistoryService

class HistoryService(IHistoryService):

    _repository: IHistoryRepository

    def __init__(self, repository: IHistoryRepository):
        self._repository = repository
    
    async def get_all_history(self) -> Iterable[History]:
       return await self._repository.get_all_history()


    async def get_history_by_user(self, user_id: int) -> Iterable[History]:
        return await self._repository.get_history_by_user(user_id)


    async def get_history_by_book(self, book_id: int) -> Iterable[History]:
        return await self._repository.get_history_by_book(book_id)


    async def update_history(self, id: int) -> None:
        return await self._repository.update_history(id)
