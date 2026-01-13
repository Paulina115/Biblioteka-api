"""A module containing book copy routers"""

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException

from src.container import Container
from src.infrastructure.services.ibook_copy import IBookCopyService
from src.core.domain.book_copy import BookCopy, BookCopyCreate, BookCopyStatus, BookCopyUpdate
from src.infrastructure.dto.userdto import UserDTO
from src.infrastructure.auth.auth import librarian_required

router = APIRouter()

@router.get("/copyid/{copy_id}", response_model=BookCopy)
@inject
async def get_book_copies_by_id(
    copy_id: int,
    service: IBookCopyService = Depends(Provide[Container.book_copy_service]),
    current_user: UserDTO = Depends(librarian_required)
) -> dict:
    """An endpoint for getting book copies by id. (Intended for Librarian use.)
    
    Args:
        copy_id: id of the book copy.
        service (IBookCopyService): The injected service dependency.
        current_user (UserDTO): The injected user authentication dependency.

    Returns:
        dict: The book copy attributes.
    """
    book = await service.get_book_copy_by_id(copy_id)
    if book:
        return book.model_dump()
    raise HTTPException(status_code=404, detail="Book copy not found")
    
@router.get("/bookid/{book_id}", response_model=list[BookCopy])
@inject
async def get_copies_by_book(
    book_id: int,
    status: BookCopyStatus | None = None,
    service: IBookCopyService = Depends(Provide[Container.book_copy_service]),
    current_user: UserDTO = Depends(librarian_required)
) -> list:
    """An endpoint for getting book copies of a specific book.(Intended for Librarian use.)
    
    Args:
        book_id: id of the book to retrive copies for.
        status (BookCopyStatus | None)
        service (IBookCopyService): The injected service dependency.
        current_user (UserDTO): The injected user authentication dependency.

    Returns:
        list: The book copy attributes collection.
    """
    copies = await service.get_copies_by_book(book_id,status)
    return copies

@router.get("/bookid/{book_id}/available-count", response_model=int)
@inject
async def count_available_copies(
    book_id: int,
    service: IBookCopyService = Depends(Provide[Container.book_copy_service]),
) -> int:
    """An endpoint counting book copies of a specific book that are available to borrow.
    
    Args:
        book_id: id of the book to count available copies for.
        service (IBookCopyService): The injected service dependency.

    Returns:
        int: Number of available book copies.
    """
    return await service.count_available_copies(book_id)

@router.post("/create", response_model=BookCopy, status_code=201)
@inject
async def add_book_copy(
    data: BookCopyCreate,
    service: IBookCopyService = Depends(Provide[Container.book_copy_service]),
    current_user: UserDTO = Depends(librarian_required)
) -> dict:
    """An endpoint for adding book copies. (Intended for Librarian use.)
    
    Args:
        data (BookCopyCreate): The book copy data.
        service (IBookCopyService): The injected service dependency.
        current_user (UserDTO): The injected user authentication dependency.

    Returns:
        dict : The book copy attributes.
    """
    copy = await service.add_book_copy(data)
    if copy:
        return copy.model_dump()
    raise HTTPException(status_code=404, detail="Copy not found")

@router.patch("/update", response_model=BookCopy)
@inject
async def update_copy(
    copy_id: int,
    data: BookCopyUpdate,
    service: IBookCopyService = Depends(Provide[Container.book_copy_service]),
    current_user: UserDTO = Depends(librarian_required)
) -> dict:
    """An endpoint for updating book copies. (Intended for Librarian use.)
    
    Args:
        copy_id (int): Id of the book copy.
        data (BookCopyUpdate): The book copy data.
        service (IBookCopyService): The injected service dependency.
        current_user (UserDTO): The injected user authentication dependency.

    Returns:
        dict: The book copy.
    """
    updated = await service.update_book_copy(copy_id, data)
    if updated:
        return updated.model_dump()
    raise HTTPException(status_code=404, detail="Book copy not found")
    
@router.delete("/delete", status_code=204)
@inject
async def delete_book_copy(
    copy_id: int,
    service: IBookCopyService = Depends(Provide[Container.book_copy_service]),
    current_user: UserDTO = Depends(librarian_required)
) -> None:
    """An endpoint for removing book copies. (Intended for Librarian use.)
    
    Args:
        copy_id: id of the book copy.
        service (IBookCopyService): The injected service dependency.
        current_user (UserDTO): The injected user authentication dependency.
    """
    result = await service.remove_book_copy(copy_id)
    if result:
        return None
    raise HTTPException(status_code=404, detail="Book copy not found")
    