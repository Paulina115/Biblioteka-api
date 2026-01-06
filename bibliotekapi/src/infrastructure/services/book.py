"""Module containing book service implementations"""

from src.core.domain.book import Book, BookCreate
from src.core.repositories.ibook import IBookRepository
from src.infrastructure.services.ibook import IBookService

class BookService(IBookService):
    """A class implementing the book service"""

    _repository: IBookRepository

    def __init__(self, repository: IBookRepository):
        self._repository = repository
    
    async def get_all_books(self) -> list[Book]:
        """The method getting all books from the repository.
        
        Returns:
            list[Book]: The collection of the all books.
        """
        return await self._repository.get_all_books()


    async def get_book_by_id(self, book_id: int) -> Book | None:
        """The method getting a book from the repository.

        Args:
            book_id (int): The id of the book.
        
        Returns:
            Book | None: The book data if exists.
        """
        return await self._repository.get_book_by_id(book_id)

    async def get_book_by_title(self, title: str) -> list[Book]:
        """The method getting book by the title from the repository.
        
        Args:
            title (str): The title of the book.
        
        Returns:
            list[Book]: The collection of the all books with this title
        """
        return await self._repository.get_book_by_title(title)

    async def get_book_by_author(self, author: str) -> list[Book]:
        """The method getting book by the author from the repository.
        
        Args:
            author (str): The author of the book.
        
        Returns:
            list[Book]: The collection of the all books written  by this author
        """
        return await self._repository.get_book_by_author(author)
        
    async def get_book_by_isbn(self, isbn: str) -> Book | None:
        """The method getting book by isbn from the repository.
        
        Args:
            isbn (str): The isbn of the book.
        
        Returns:
            Book | None: The book data if exist.
        """
        return await self._repository.get_book_by_isbn(isbn)
    
    async def filter_books(
        self, 
        author: str | None = None,
        subject: str | None = None,
        publisher: str | None = None,
        publication_year: int | None = None,
        language: str | None = None,
    ) -> list[Book]:
        """The method getting filtered books by chosen parameter
        
        Args:
            author: str | None = None,
            subject: str | None = None,
            publisher: str | None = None,
            publication_year: int | None = None,
            language: str | None = None,
        
        Returns:
            list[Book]: The collection of the all books which match the parameters.
        """
        return await self._repository.filter_books(author, subject, publisher, publication_year, language)


    async def add_book(self, data: BookCreate, copies_count: int = 1) -> Book | None:
        """The method adding new book to the repository.
            Also creates the specified number of copies (BookCopy) for this book.
        
        Args:
            data (BookCreate): The attributes of the book.
            copies_count (int): Number of copies to create (default=1)
        Returns:
            Book | None: The newly created book.
        """
        return await self._repository.add_book(data, copies_count)

    async def update_book(self, book_id: int, data: BookCreate) -> Book | None:
        """The method updating book data in the repository.
        
        Args:
            book_id (int): The book id.
            data (BookCreate): The attributes of the book.

        Returns:
            Book | None: The updated book.
        """
        return await self._repository.update_book(book_id,data)


    async def remove_book(self, book_id: int) -> bool:
        """The method removing book and all its copies (BookCopy)  from the repository.

        Args:
            book_id (int): The book id.

        Returns:
            bool: Success of the operation.
        """
        return await self._repository.delete_book(book_id)

    

    
    


    