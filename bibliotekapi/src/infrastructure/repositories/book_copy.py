"""Module containing book copy repository implementation"""

from sqlalchemy import select, update, delete, func
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.repositories.ibook_copy import IBookCopyRepository
from src.core.domain.book_copy import BookCopy as BookCopyDomain, BookCopyCreate, BookCopyStatus
from src.db import BookCopy as BookCopyORM, async_session_factory


class BookCopyRepository(IBookCopyRepository):
    """A class implementing the book copy repository."""
    def __init__(self, sessionmaker = async_session_factory):
        self._sessionmaker = sessionmaker

    async def count_available_copies(self, book_id: int) -> int:
        """the method counting how many copies of the book is available.

            Args:
                book_id (int): The id of the book.

            Returns:
                int: The number of available copies of the book.
        """
        async with self._sessionmaker() as session:
            stmt = (
                select(func.count(BookCopyORM.copy_id))
                .where(BookCopyORM.book_id==book_id,
                       BookCopyORM.status==BookCopyStatus.available)
            )
            return await session.scalar(stmt) or 0



    async def get_book_copy_by_id(self, copy_id: int) -> BookCopyDomain | None:
        """The method getting a book copy from the data storage.

        Args:
            copy_id (int): The id of the book copy.
        Returns:
            BookCopyDomain | None: The book copy data if exists.
        """
        async with self._sessionmaker() as session:
            copy = await self._get_by_id(copy_id, session)
            return BookCopyDomain.model_validate(copy) if  copy else None
        
    async def get_copies_by_book(self, book_id: int, status: BookCopyStatus | None = None) -> list[BookCopyDomain]:
        """The method getting book copies of a specific book from the data storage.
            Optionally filter by status.

        Args:
            book_id (int): The id of the book to retrive copies for.
            status (BookCopyStatus | None): status of the copy e.g available.

        Returns:
            list[BookCopyDomain]: The collection of the all copies of a specific book.
        """
        async with self._sessionmaker() as session:
            stmt = select(BookCopyORM).where(BookCopyORM.book_id==book_id)
            if status is not None:
                stmt = stmt.where(BookCopyORM.status==status)
            copies = (await session.scalars(stmt)).all()
            return [BookCopyDomain.model_validate(copy) for copy in copies]

    async def add_book_copy(self, data: BookCopyCreate) -> BookCopyDomain | None:
        """The method adding new book copy to the data storage.
            
        Args:
            data (BookCopyCreate): The attributes of the book copy.
        Returns:
            BookCopyDomain | None: The newly created book copy.
        """
        async with self._sessionmaker() as session:
            new_copy = BookCopyORM(**data.model_dump())
            session.add(new_copy)
            await session.commit()
            return BookCopyDomain.model_validate(new_copy) if new_copy else None

    async def update_book_copy(self, copy_id: int, data: BookCopyCreate) -> BookCopyDomain | None:
        """The method updating book copy  data in the data storage.
        
        Args:
            copy_id (int): The book copy  id.
            data (BookCopyCreate): The attributes of the book copy.

        Returns:
            BookCopyDomain | None: The updated book copy.
        """
        async with self._sessionmaker() as session:
            copy = await self._get_by_id(copy_id, session)
            if copy:
                for field, value in data.model_dump().items():
                    setattr(copy,field,value)
                await session.commit()
                return BookCopyDomain.model_validate(copy)
            return None



    async def delete_book_copy(self, copy_id: int) -> bool:
        """The method removing book copy from the data storage.

        Args:
            copy_id (int): The book copy id.

        Returns:
            bool: Success of the operation.
        """
        async with self._sessionmaker() as session:
            copy = await self._get_by_id(copy_id, session)
            if copy:
                await session.delete(copy)
                await session.commit()
                return True
            return False

    async def _get_by_id(self, copy_id: int, session: AsyncSession) -> BookCopyORM| None:
        """A private method getting book copy from the DB based on its ID.

        Args:
            copy_id (int): The ID of the book copy.
            session (AsyncSession): session for query.

        Returns:
            BookCopyORM | None: Book copy record if exists.
        """
        return await session.get(BookCopyORM, copy_id)
        
    