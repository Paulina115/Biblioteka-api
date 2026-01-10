"""A module containing book routers"""

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException

from src.container import Container
from src.infrastructure.services.ibook import IBookService
from src.core.domain.book import Book, BookCreate
from src.infrastructure.dto.userdto import UserDTO
from src.infrastructure.auth.auth import librarian_required

router = APIRouter()


@router.get("/all", response_model=list[Book])
@inject
async def get_all_books(
    service: IBookService = Depends(Provide[Container.book_service]),
) -> list:
    """An endpoint for getting all books
    
    Args:
        service (IBookService): The injected service dependency.

    Returns:
        list: The book attributes collections.
    """
    books = await service.get_all_books()
    return books


@router.get("/bookid/{book_id}", response_model=Book)
@inject
async def get_book_by_id(
    book_id: int,
    service: IBookService = Depends(Provide[Container.book_service]),
    current_user: UserDTO = Depends(librarian_required)
) -> dict:
    """An endpoint for getting book by id. (Intended for Librarian use.)
    
    Args:
        book_id (int): The book id.
        service (IBookService): The injected service dependency.
        current_user (UserDTO): The injected user authentication dependency.

    Returns:
        dict: The book attributes.
    """
    book = await service.get_book_by_id(book_id)
    if book:
        return book.model_dump()
    raise HTTPException(status_code=404, detail="Book not found")

@router.get("/title/{title}", response_model=list[Book])
@inject
async def get_by_title(
    title: str,
    service: IBookService = Depends(Provide[Container.book_service]),
) -> list:
    """An endpoint for getting book by title.
    
    Args:
        title (int): The book title.
        service (IBookService): The injected service dependency.

    Returns:
        dict: The book attributes.
    """
    books = await service.get_book_by_title(title)
    if books:
        return books
    raise HTTPException(status_code=404, detail="Book not found")

@router.get("/author/{author}", response_model=list[Book])
@inject
async def get_by_author(
    author: str,
    service: IBookService = Depends(Provide[Container.book_service]),
) -> list:
    """An endpoint for getting books by author.
    
    Args:
        author (int): The book author.
        service (IBookService): The injected service dependency.

    Returns:
        list: The book attributes collections.
    """
    books = await service.get_book_by_author(author)
    if books:
        return books
    raise HTTPException(status_code=404, detail="Book not found")

@router.get("/isbn/{isbn}", response_model=Book)
@inject
async def get_by_isbn(
    isbn: str,
    service: IBookService = Depends(Provide[Container.book_service]),
) -> dict:
    """An endpoint for getting book by isbn.
    
    Args:
        isbn (int): The book isbn.
        service (IBookService): The injected service dependency.

    Returns:
        dict: The book attributes.
    """
    book = await service.get_book_by_isbn(isbn)
    if book:
        return book.model_dump()
    raise HTTPException(status_code=404, detail="Book not found")

@router.get("/filter", response_model=list[Book])
@inject
async def filter_by_category(
    author: str | None = None,
    subject: str | None = None,
    publisher: str | None = None,
    publication_year: int | None = None,
    language: str | None = None,
    service: IBookService = Depends(Provide[Container.book_service]),
) -> list:
    """An endpoint filtering books by given atribute/s.
    
    Args:
        author (str | None): The book author.
        subject (str | None): The book subject.
        publisher (str | None): The book publisher. 
        publication_year (int | None): The book publication year.
        language (str | None): The book language.
        service (IBookService): The injected service dependency.

    Returns:
        list: The book attributes collection.
    """
    books = await service.filter_books(
        author=author,
        subject=subject,
        publisher=publisher,
        publication_year=publication_year,
        language=language,
    )
    if books:
        return books
    raise HTTPException(status_code=404, detail="Books not found")
    

@router.post("/create", response_model=Book, status_code=201)
@inject
async def create_book(
    data: BookCreate,
    service: IBookService = Depends(Provide[Container.book_service]),
    current_user: UserDTO = Depends(librarian_required)
) -> dict :
     """An endpoint for creating new book. (Intended for Librarian use.)
    
    Args:
        data (BookCreate): The book data.
        service (IBookService): The injected service dependency.
        current_user (UserDTO): The injected user authentication dependency.

    Returns:
        dict: The created book attributes.
    """
     return await service.add_book(data)

@router.put("/update", response_model=Book)
@inject
async def update_book(
    book_id: int,
    data: BookCreate,
    service: IBookService = Depends(Provide[Container.book_service]),
    current_user: UserDTO = Depends(librarian_required)
) -> dict :
     """An endpoint for updating book. (Intended for Librarian use.)
    
    Args:
        book_id (int): The book id.
        data (BookCreate): Data for updating the book.
        service (IBookService): The injected service dependency.
        current_user (UserDTO): The injected user authentication dependency.

    Returns:
        dict: The updated book attributes.
    """
     updated = await service.update_book(book_id, data)
     if not updated:
        raise HTTPException(status_code=404, detail="Book not found")
     return updated


@router.delete("/delete", status_code=204)
@inject
async def delete_book(
    book_id: int,
    service: IBookService = Depends(Provide[Container.book_service]),
    current_user: UserDTO = Depends(librarian_required)
) -> None:
     """An endpoint for deleting book. (Intended for Librarian use.)
    
    Args:
        book_id (int): The book id.
        service (IBookService): The injected service dependency.
        current_user (UserDTO): The injected user authentication dependency.
    """
     result = await service.remove_book(book_id)
     if not result:
        raise HTTPException(status_code=404, detail="Book not found")
     return None
