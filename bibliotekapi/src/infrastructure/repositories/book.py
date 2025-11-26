from typing import Any, Iterable

from sqlalchemy import select,join

from core.repositories.ibook import IBookRepository
from core.domain.book import Book
from src.db import (
    book_table,
    database,
)
from src.infrastructure.dto.bookdto import BookDTO


class BookRepository(IBookRepository):

    async def get_all_books(self) -> Iterable[Book]:
        
        query = (
            select(book_table)
        )
        books = await database.fetch_all(query)

        return [BookDTO.from_record(book) for book in books]

    async def get_book_by_id(self, id: int) -> Book | None:
        query = ( 
            select(book_table).where(book_table.id == id)
        )
        book = await database.fetch_one(query)
        
        return BookDTO.from_record(book) if book else None

    async def get_by_title(self, title: str) -> Book | None:
        query = ( 
            select(book_table).where(book_table.title == title)
        )
        book = await database.fetch_one(query)

        return BookDTO.from_record(book) if book else None


    async def get_by_author(self, author: str) -> Iterable[Book] | None:
        query = (
            select(book_table).where(book_table.author == author)
        )
        books = await database.fetch_all(query)

        return [BookDTO.from_record(book) for book in books]

        

    async def get_by_isbn(self, isbn: str) -> Book | None:
        query = (
            select(book_table).where(book_table.isbn == isbn)
        )
        book = await database.fetch_one(query)

        return BookDTO.from_record(book) if book else None

    
    async def filter_by_category(self, category: str) -> Iterable[Book]:
        query = (
            select(book_table).where(book_table.category == category)
        )
        books = await database.fetch_all(query)

        return [BookDTO.from_record(book) for book in books]


    async def add_book(self, book: Book) -> None:
        query = (
            Book.insert().values()
        )

    async def update_book(self, id: int,data: Book) -> None:
        pass

    async def delete_book(self, book: Book) -> None:
        pass



    
