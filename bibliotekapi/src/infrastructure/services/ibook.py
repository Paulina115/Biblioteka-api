"""Module containing book service abstractions"""

from abc import ABC, abstractmethod

from src.core.domain.book import Book, BookCreate

class IBookService(ABC):
    """An abstract class representing protocol of book service"""

    @abstractmethod
    async def get_all_books(self) -> list[Book]:
        """The abstract getting all books from the repository.
        
        Returns:
            list[Book]: The collection of the all books.
        """

    @abstractmethod
    async def get_book_by_id(self, book_id: int) -> Book | None:
        """The abstract getting a book from the repository.

        Args:
            book_id (int): The id of the book.
        
        Returns:
            Book | None: The book data if exists.
        """

    @abstractmethod
    async def get_book_by_title(self, title: str) -> list[Book]:
        """The abstract getting book by the title from the repository.
        
        Args:
            title (str): The title of the book.
        
        Returns:
            list[Book]: The collection of the all books with this title
        """

    @abstractmethod
    async def get_book_by_author(self, author: str) -> list[Book]:
        """The abstract getting book by the author from the repository.
        
        Args:
            author (str): The author of the book.
        
        Returns:
            list[Book]: The collection of the all books written  by this author
        """

    @abstractmethod
    async def get_book_by_isbn(self, isbn: str) -> Book | None:
        """The abstract getting book by isbn from the repository.
        
        Args:
            isbn (str): The isbn of the book.
        
        Returns:
            Book | None: The book data if exist.
        """
    
    
    @abstractmethod
    async def filter_books(
        self, 
        author: str | None = None,
        subject: str | None = None,
        publisher: str | None = None,
        publication_year: int | None = None,
        language: str | None = None,
    ) -> list[Book]:
        """The abstract getting filtered books by chosen parameter
        
        Args:
            author: str | None = None,
            subject: str | None = None,
            publisher: str | None = None,
            publication_year: int | None = None,
            language: str | None = None,
        
        Returns:
            list[Book]: The collection of the all books which match the parameters.
        """

    @abstractmethod
    async def add_book(self, data: BookCreate, copies_count: int = 1) -> Book | None:
        """The abstract adding new book to the repository.
            Also creates the specified number of copies (BookCopy) for this book.
        
        Args:
            data (BookCreate): The attributes of the book.
            copies_count (int): Number of copies to create (default=1)
        Returns:
            Book | None: The newly created book.
        """

    @abstractmethod
    async def update_book(self, book_id: int, data: BookCreate) -> Book | None:
        """The abstract updating book data in the repository.
        
        Args:
            book_id (int): The book id.
            data (BookCreate): The attributes of the book.

        Returns:
            Book | None: The updated book.
        """

    @abstractmethod
    async def remove_book(self, book_id: int) -> bool:
        """The abstract removing book and all its copies (BookCopy)  from the repository.

        Args:
            book_id (int): The book id.

        Returns:
            bool: Success of the operation.
        """
    