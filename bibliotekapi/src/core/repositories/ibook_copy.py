"""Module containing book copy repository abstractions"""

from abc import ABC, abstractmethod

from src.core.domain.book_copy import BookCopyCreate, BookCopy, BookCopyStatus


class IBookCopyRepository(ABC):
    """An abstract class representing protocol of book copy  repository"""

    @abstractmethod
    async def get_book_copy_by_id(self, copy_id: int) -> BookCopy | None:
        """The abstract getting a book copy from the data storage.

        Args:
            copy_id (int): The id of the book copy.
        
        Returns:
            BookCopy | None: The book copy data if exists.
        """

    @abstractmethod
    async def get_copies_by_book(self, book_id: int, status: BookCopyStatus | None = None) -> list[BookCopy]:
        """The abstract getting book copies of a specific book from the data storage.
            Optionally filter by status.

        Args:
            book_id (int): The id of the book to retrive copies for.
            status (BookCopy | None): status of the copy e.g available.

        Returns:
            list[BookCopy]: The collection of the all copies of a specific book.
        """

    @abstractmethod
    async def add_book(self, data: BookCopyCreate) -> BookCopy | None:
        """The abstract adding new book copy to the data storage.
            
        Args:
            data (BookCopyCreate): The attributes of the book copy.
        Returns:
            BookCopy | None: The newly created book copy.
        """

    @abstractmethod
    async def update_book_copy(self, copy_id: int, data: BookCopyCreate) -> BookCopy | None:
        """The abstarct updating book copy  data in the data storage.
        
        Args:
            copy_id (int): The book copy  id.
            data (BookCopyCreate): The attributes of the book copy.

        Returns:
            BookCopy | None: The updated book copy.
        """

    @abstractmethod
    async def delete_book_copy(self, copy_id: int) -> bool:
        """The abstarct removing book copy from the data storage.

        Args:
            copy_id (int): The boo copy id.

        Returns:
            bool: Success of the operation.
        """

