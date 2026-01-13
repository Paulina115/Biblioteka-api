"""Module containing book repository implementation"""

from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.repositories.ibook import IBookRepository
from src.core.domain.book import Book as BookDomain, BookCreate
from src.db import Book as BookORM

class BookRepository(IBookRepository):
    """A class implementing the book repository."""
    
    def __init__(self, session: AsyncSession):
        self._session = session
    
    async def get_all_books(self) -> list[BookDomain]:
        """The method getting all books from the data storage.
        
        Returns:
            list[BookDomain]: The collection of the all books.
        """
        stmt = select(BookORM)
        books = (await self._session.scalars(stmt)).all()
        return [BookDomain.model_validate(book) for book in books] 

    async def get_book_by_id(self, book_id: int) -> BookDomain | None:
        """The method getting a book from the data storage.

        Args:
            book_id (int): The id of the book.
        
        Returns:
            BookDomain | None: The book data if exists.
        """
        book = await self._get_by_id(book_id)
        return BookDomain.model_validate(book) if  book else None

    async def get_book_by_title(self, title: str) -> list[BookDomain]:
        """The method getting book by the title from the data storage.
        
        Args:
            title (str): The title of the book.
        
        Returns:
            list[BookDomain]: The collection of the all books with this title
        """
        stmt = select(BookORM).where(BookORM.title == title)
        books = (await self._session.scalars(stmt)).all()
        return [BookDomain.model_validate(book) for book in books]

    async def get_book_by_author(self, author: str) -> list[BookDomain]:
        """The method getting book by the author from the data storage.
        
        Args:
            author (str): The author of the book.
        
        Returns:
            list[Book]: The collection of the all books written  by this author
        """
        stmt = select(BookORM).where(BookORM.authors.any(author))
        books = (await self._session.scalars(stmt)).all()
        return [BookDomain.model_validate(book) for book in books]

    async def get_book_by_isbn(self, isbn: str) -> BookDomain | None:
        """The method getting book by isbn from the data storage.
        
        Args:
            isbn (str): The isbn of the book.
        
        Returns:
            BookDomain | None: The book data if exist.
        """
        stmt = select(BookORM).where(BookORM.isbn == isbn)
        book = (await self._session.scalars(stmt)).first()
        return BookDomain.model_validate(book) if book else None 
    
    async def filter_books(
        self, 
        author: str | None = None,
        subject: str | None = None,
        publisher: str | None = None,
        publication_year: int | None = None,
        language: str | None = None,
    ) -> list[BookDomain]:
        """The method getting filtered books by chosen parameter
        
        Args:
            author: str | None = None,
            subject: str | None = None,
            publisher: str | None = None,
            publication_year: int | None = None,
            language: str | None = None,
        
        Returns:
            list[BookDomain]: The collection of the all books which match the parameters.
        """
        stmt = select(BookORM)
        conditions = []

        if author:
            conditions.append(BookORM.authors.any(author))
        if subject:
            conditions.append(BookORM.subject.any(subject))
        if publisher:
            conditions.append(BookORM.publisher == publisher)
        if publication_year:
            conditions.append(BookORM.publication_year == publication_year)
        if language:
            conditions.append(BookORM.language == language)

        if conditions:
            stmt = stmt.where(*conditions)

        result = await self._session.scalars(stmt)
        books = result.all()
        return [BookDomain.model_validate(book) for book in books]

    async def add_book(self, data: BookCreate, copies_count: int = 1) -> BookDomain | None:
        """The method adding new book to the data storage.
        
        Args:
            data (BookCreate): The attributes of the book.
        Returns:
            BookDomain | None: The newly created book.
        """
        new_book = BookORM(**data.model_dump())
        self._session.add(new_book)
        
        await self._session.flush()

        return BookDomain.model_validate(new_book)  if new_book else None
            

    async def update_book(self, book_id: int, data: BookDomain) -> BookDomain | None:
        """The method updating book data in the data storage.
        
        Args:
            book_id (int): The book id.
            data (BookDomain): The attributes of the book.

        Returns:
            BookDomain | None: The updated book.
        """
        book = await self._get_by_id(book_id)
        if book:
            for field, value in data.model_dump(exclude_unset=True).items():
                setattr(book, field, value)
            await self._session.flush()
            return BookDomain.model_validate(book)
        return None

    async def delete_book(self, book_id: int) -> bool:
        """The method removing book and all its copies (BookCopy)  from the data storage.

        Args:
            book_id (int): The book id.

        Returns:
            bool: Success of the operation.
        """
        book = await self._get_by_id(book_id)
        if book:
            await self._session.delete(book)
            await self._session.flush()
            return True
        return False

    async def _get_by_id(self, book_id: int) -> BookORM| None:
        """A private method getting book from the DB based on its ID.

        Args:
            book_id (int): The ID of the book.

        Returns:
            BookORM | None: Book record if exists.
        """
        return await self._session.get(BookORM, book_id)
        
    
