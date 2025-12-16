from typing import Any, Iterable

from asyncpg import Record  # type: ignore
from sqlalchemy import select,join

from src.core.repositories.ibook import IBookRepository
from src.core.domain.book import Book
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
            select(book_table).where(book_table.c.id == id)
        )
        book = await database.fetch_one(query)
        
        return BookDTO.from_record(book) if book else None

    async def get_by_title(self, title: str) -> Book | None:
        query = ( 
            select(book_table).where(book_table.c.title == title)
        )
        book = await database.fetch_one(query)

        return BookDTO.from_record(book) if book else None


    async def get_by_author(self, author: str) -> Iterable[Book] | None:
        query = (
            select(book_table).where(book_table.c.author == author)
        )
        books = await database.fetch_all(query)

        return [BookDTO.from_record(book) for book in books]

        

    async def get_by_isbn(self, isbn: str) -> Book | None:
        query = (
            select(book_table).where(book_table.c.isbn == isbn)
        )
        book = await database.fetch_one(query)

        return BookDTO.from_record(book) if book else None

    
    async def filter_by_category(self, category: str) -> Iterable[Book]:
        query = (
            select(book_table).where(book_table.category == category)
        )
        books = await database.fetch_all(query)

        return [BookDTO.from_record(book) for book in books]


    async def add_book(self, book: Book) -> Book | None:
        query = (
            book_table.insert().values(**book.__dict__)
        )
        new_book_id = await database.execute(query)
        new_book = await self.get_book_by_id(new_book_id)

        return Book(**dict(new_book)) if new_book else None


    async def update_book(self, id: int,data: Book) -> None:
        if self.get_book_by_id(id):
            query = (
                book_table.update()
                .where(book_table.c.id == id)
                .values(**data.model_dump())
            )
            await database.execute(query)
        
            book = await self.get_book_by_id(id)

            return Book(**dict(book)) if book else None
        return None



    async def delete_book(self, book_id: int) -> None:
        if self._get_book_by_id(book_id):
            query = ( book_table
            .delete()
            .where(book_table.c.id == book_id)
            )
            await database.execute(query)

            return True 
        return False
    async def _get_book_by_id(self, id: int) -> Record | None:
        query = (
            book_table.select()
            .where(book_table.c.id == id)
            .order_by(book_table.c.title.asc())
        )

        return await database.fetch_one(query)




    
