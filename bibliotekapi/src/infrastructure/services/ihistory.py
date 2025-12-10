from abc import ABC, abstractmethod
from typing import Iterable

from src.core.domain.history import History
from src.infrastructure.dto.historydto import HistoryDTO


class IHistoryService(ABC):

    @abstractmethod
    async def get_all_history(self) -> Iterable[History]:
        pass

    @abstractmethod
    async def get_history_by_user(self, user_id: int) -> Iterable[History]:
        pass

    @abstractmethod
    async def get_history_by_book(self, book_id: int) -> Iterable[History]:
        pass

    @abstractmethod
    async def update_history(self, id: int) -> None:
        pass

    