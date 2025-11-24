from abc import ABC, abstractmethod
from typing import Iterable

from bibliotekapi.core.domain.book import Book


class IBookRepository(ABC):

    @abstractmethod
    async def get_all_books(self) -> Iterable[Book]:
        pass

    @abstractmethod
    async def get_book_by_id(self, id: int) -> Book:
        pass

    @abstractmethod
    async def get_by_title(self, title: str) -> Book:
        pass

    @abstractmethod
    async def get_by_author(self, author: str) -> Book:
        pass

    @abstractmethod
    async def get_by_isbn(self, isbn: str) -> Book:
        pass
    
    @abstractmethod
    async def filter_by_category(self, category: str) -> Iterable[Book]:
        pass

    @abstractmethod
    async def add_book(self, book: Book) -> None:
        pass

    @abstractmethod
    async def update_book(self, id: int,data: Book) -> None:
        pass

    @abstractmethod
    async def delete_book(self, book: Book) -> None:
        pass

