from typing import Any, Iterable

from sqlalchemy import select,join

from core.repositories.ibook import IBookRepository
from core.domain.book import Book


class BookRepository(IBookRepository):

    async def get_all_books(self) -> Iterable[Book]:
        
        query = (
            select(Book)
        )
    # books = await database.fetch_all(query)

    async def get_book_by_id(self, id: int) -> Iterable[Book]:
        query = ( 
            select(Book).where(Book.id == id)
        )

    async def get_by_title(self, title: str) -> Book:
        query = ( 
            select(Book).where(Book.title == title)
        )

    async def get_by_author(self, author: str) -> Book:
        query = (
            select(Book).where(Book.author == author)
        )

    async def get_by_isbn(self, isbn: str) -> Book:
        query = (
            select(Book).where(Book.isbn == isbn)
        )
    
    async def filter_by_category(self, category: str) -> Iterable[Book]:
        query = (
            select(Book).where(Book.category == category)
        )

    async def add_book(self, book: Book) -> None:
        query = (
            Book.insert().values()
        )

    async def update_book(self, id: int,data: Book) -> None:
        pass

    async def delete_book(self, book: Book) -> None:
        pass



    
