from typing import Any, Iterable

from asyncpg import Record  # type: ignore
from sqlalchemy import select,join

from core.repositories.ihistory import IHistoryRepository
from core.domain.history import History
from src.db import (
    history_table,
    user_table,
    database,
)
from src.infrastructure.dto.historydto import HistoryDTO


class HistoryRepository(IHistoryRepository):
    async def get_all_history(self) -> Iterable[History]:
        query = (
            select(history_table)
        )
        history = await database.fetch_all(query)

        return [HistoryDTO.from_record(his) for his in history]

    async def get_history_by_user(self, user_id: int) -> Iterable[History]:
        query = ( 
            select(history_table)
            .where(history_table.user_id == user_id)
        )
        history = await database.fetch_one(query)
        
        return HistoryDTO.from_record(history) if history else None

    async def get_history_by_book(self, book_id: int) -> Iterable[History]:
        query = ( 
            select(history_table)
            .where(history_table.book_id == book_id)
        )
        history = await database.fetch_one(query)
        
        return HistoryDTO.from_record(history) if history else None

    async def update_history(self, id: int, data: History) -> None:
        if self.get_history_by_id(id):
            query = (
                history_table.update()
                .where(history_table.c.id == id)
                .values(**data.model_dump())
            )
            await database.execute(query)
        
        new_history = await self.get_history_by_id(id)

        return History(**dict(new_history)) if new_history else None
    
    async def _get_history_by_id(self, id: int) -> Record | None:
        query = (
            history_table.select()
            .where(history_table.c.id == id)
        )

        return await database.fetch_one(query)