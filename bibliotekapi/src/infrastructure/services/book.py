
from typing import Iterable

from src.core.domain.book import Book
from src.core.repositories.ibook import IBookRepository
from src.infrastructure.services.ibook import IBookService

class BookService(IBookService):

    _repository: IBookRepository

    def __init__(self, repository: IBookRepository):
        self._repository = repository
    
    
    async def get_all_books(self) -> Iterable[Book]:
        return await self._repository.get_all_books()


    
    async def get_book_by_id(self, id: int) -> Book:
        return await self._repository.get_book_by_id(id)


   
    async def get_by_title(self, title: str) -> Book:
        return await self._repository.get_by_title(title)

    
    async def get_by_author(self, author: str) -> Book:
        return await self._repository.get_by_author(author)


    
    async def get_by_isbn(self, isbn: str) -> Book:
        return await self._repository.get_by_isbn(isbn)

    
    
    async def filter_by_category(self, category: str) -> Iterable[Book]:
        return await self._repository.filter_by_category(category)


   
    async def add_book(self, book: Book) -> None:
        return await self._repository.add_book(book)


    
    async def update_book(self, id: int,data: Book) -> None:
        return await self._repository.update_book(id,data)


    
    async def delete_book(self, book: Book) -> None:
       return await self._repository.delete_book(book)


    