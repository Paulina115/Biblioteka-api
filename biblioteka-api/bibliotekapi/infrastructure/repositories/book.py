from typing import Any, Iterable

from core.repositories.ibook import IBookRepository
from core.domain.book import Book


class BookRepository(IBookRepository):

    async def get_all_books(self) -> Iterable[Book]:
        
        query = (
            
        )
