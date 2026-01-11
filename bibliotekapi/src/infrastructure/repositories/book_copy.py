"""Module containing book copy repository implementation"""

from sqlalchemy import select, update, delete, func
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.repositories.ibook_copy import IBookCopyRepository
from src.core.domain.book_copy import BookCopy as BookCopyDomain, BookCopyCreate, BookCopyStatus
from src.db import BookCopy as BookCopyORM


class BookCopyRepository(IBookCopyRepository):
    """A class implementing the book copy repository."""
    
    def __init__(self, session : AsyncSession):
        self._session = session

    async def count_available_copies(self, book_id: int) -> int:
        """the method counting how many copies of the book is available.

            Args:
                book_id (int): The id of the book.

            Returns:
                int: The number of available copies of the book.
        """
        
        stmt = (
            select(func.count(BookCopyORM.copy_id))
            .where(BookCopyORM.book_id==book_id,
                BookCopyORM.status==BookCopyStatus.available)
        )
        return await self._session.scalar(stmt) or 0

    async def get_book_copy_by_id(self, copy_id: int) -> BookCopyDomain | None:
        """The method getting a book copy from the data storage.

        Args:
            copy_id (int): The id of the book copy.
        Returns:
            BookCopyDomain | None: The book copy data if exists.
        """
        copy = await self._get_by_id(copy_id)
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
        stmt = select(BookCopyORM).where(BookCopyORM.book_id==book_id)
        if status is not None:
            stmt = stmt.where(BookCopyORM.status==status)
        copies = (await self._session.scalars(stmt)).all()
        return [BookCopyDomain.model_validate(copy) for copy in copies]

    async def add_book_copy(self, data: BookCopyCreate) -> BookCopyDomain | None:
        """The method adding new book copy to the data storage.
            
        Args:
            data (BookCopyCreate): The attributes of the book copy.
        Returns:
            BookCopyDomain | None: The newly created book copy.
        """
        new_copy = BookCopyORM(**data.model_dump())
        self._session.add(new_copy)
        await self._session.flush()
        return BookCopyDomain.model_validate(new_copy) if new_copy else None

    async def update_book_copy(self, copy_id: int, data: BookCopyDomain) -> BookCopyDomain | None:
        """The method updating book copy  data in the data storage.
        
        Args:
            copy_id (int): The book copy  id.
            data (BookCopyDomain): The attributes of the book copy.

        Returns:
            BookCopyDomain | None: The updated book copy.
        """
        copy = await self._get_by_id(copy_id)
        if copy:
            for field, value in data.model_dump(exclude_unset=True).items():
                setattr(copy,field,value)
            await self._session.flush()
            return BookCopyDomain.model_validate(copy)
        return None

    async def delete_book_copy(self, copy_id: int) -> bool:
        """The method removing book copy from the data storage.

        Args:
            copy_id (int): The book copy id.

        Returns:
            bool: Success of the operation.
        """
        copy = await self._get_by_id(copy_id)
        if copy:
            await self._session.delete(copy)
            await self._session.flush()
            return True
        return False

    async def _get_by_id(self, copy_id: int) -> BookCopyORM | None:
        """A private method getting book copy from the DB based on its ID.

        Args:
            copy_id (int): The ID of the book copy.

        Returns:
            BookCopyORM | None: Book copy record if exists.
        """
        return await self._session.get(BookCopyORM, copy_id)
        
    