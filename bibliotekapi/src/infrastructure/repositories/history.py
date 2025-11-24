from typing import Any, Iterable

from sqlalchemy import select,join

from core.repositories.ihistory import IHistoryRepository
from core.domain.history import History


class HistoryRepository(IHistoryRepository):
    async def get_all_history(self) -> Iterable[History]:
        query = ( 
            select(History)
        )

    async def get_history_by_user(self, user_id: int) -> Iterable[History]:
        query = ( 
            select(History).join(User).
        )

    async def get_history_by_book(self, book_id: int) -> Iterable[History]:
        query = ( 
            select(Book).where(Bo
        )

    async def update_history(self, id: int) -> None:
        pass