"""Module containing book copy service implementation"""

from src.core.domain.book_copy import BookCopy, BookCopyCreate, BookCopyStatus, BookCopyUpdate
from src.core.repositories.ibook_copy import IBookCopyRepository
from src.infrastructure.services.ibook_copy import IBookCopyService
from src.infrastructure.services.iunit_of_work import IUnitOfWork

class BookCopyService(IBookCopyService):
    """A class implementing the book copy service"""
    
    _repository: IBookCopyRepository

    def __init__(self, repository: IBookCopyRepository, uow: IUnitOfWork):
        self._repository = repository
        self._uow = uow
    
    async def count_available_copies(self, book_id: int) -> int:
        """the method checking how many copies of the book is available.

            Args:
                book_id (int): The id of the book.

            Returns:
                int: The number of available copies of the book.
        """
        return await self._repository.count_available_copies(book_id)

    async def get_book_copy_by_id(self, copy_id: int) -> BookCopy | None:
        """The method getting a book copy from the repository. (Intended for librarian use).

        Args:
            copy_id (int): The id of the book copy.
        
        Returns:
            BookCopy | None: The book copy data if exists.
        """
        return await self._repository.get_book_copy_by_id(copy_id)


    async def get_copies_by_book(self, book_id: int, status: BookCopyStatus | None = None, ) -> list[BookCopy]:
        """The method getting book copies of a specific book from the repository. (Intended for librarian use).
            Optionally filter by status.

        Args:
            book_id (int): The id of the book to retrieve copies for.
            status (BookCopyStatus | None): status of the copy e.g available.

        Returns:
            list[BookCopy]: The collection of the all copies of a specific book.
        """
        return await self._repository.get_copies_by_book(book_id, status)

    async def add_book_copy(self, data: BookCopyCreate) -> BookCopy | None:
        """The method adding new book copy to the repository. (Intended for librarian use).
            
        Args:
            data (BookCopyCreate): The attributes of the book copy.
        Returns:
            BookCopy | None: The newly created book copy.
        """
        async with self._uow:
            new_copy = await self._uow.copy_repository.add_book_copy(data)
            if not new_copy:
                return None
            return new_copy

    async def update_book_copy(self, copy_id: int, data: BookCopyUpdate) -> BookCopy | None:
        """The abstract updating book copy  data in the repository.(Intended for librarian use).
        
        Args:
            copy_id (int): The book copy  id.
            data (BookCopyUpdate): The attributes of the book copy.

        Returns:
            BookCopy | None: The updated book copy.
        """
        async with self._uow:
            updated_copy = await self._uow.copy_repository.update_book_copy(copy_id, data)
            if not updated_copy:
                return None
            return updated_copy

    async def remove_book_copy(self, copy_id: int) -> bool:
        """The abstract removing book copy from the repository. (Intended for librarian use).

        Args:
            copy_id (int): The book copy id.

        Returns:
            bool: Success of the operation.
        """
        async with self._uow:
            copy = await self._uow.copy_repository.delete_book_copy(copy_id)
            if not copy:
                return False
            return True