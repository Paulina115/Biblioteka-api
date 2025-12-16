from typing import Iterable

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException

from src.container import Container
from src.infrastructure.services.ibook import IBookService
from src.infrastructure.dto.bookdto import BookDTO
from src.core.domain.book import Book

router = APIRouter()


@router.get("/all", response_model=Iterable[BookDTO])
@inject
async def get_all_books(
    service: IBookService = Depends(Provide[Container.book_service]),
):
    books = await service.get_all_books()
    return books


@router.get("/{book_id}", response_model=BookDTO)
@inject
async def get_book_by_id(
    book_id: int,
    service: IBookService = Depends(Provide[Container.book_service]),
):
    book = await service.get_book_by_id(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@router.get("/{title}", response_model=BookDTO)
@inject
async def get_by_title(
    title: str,
    service: IBookService = Depends(Provide[Container.book_service]),
):
    book = await service.get_by_title(title)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@router.get("/{author}", response_model=BookDTO)
@inject
async def get_by_author(
    author: str,
    service: IBookService = Depends(Provide[Container.book_service]),
):
    book = await service.get_by_author(author)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book
@router.get("/{isbn}", response_model=BookDTO)
@inject
async def get_by_isbn(
    isbn: str,
    service: IBookService = Depends(Provide[Container.book_service]),
):
    book = await service.get_by_isbn(isbn)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book
@router.get("/{category}", response_model=BookDTO)
@inject
async def filter_by_category(
    category: str,
    service: IBookService = Depends(Provide[Container.book_service]),
):
    book = await service.filter_by_category(category)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@router.post("/create", response_model=Book, status_code=201)
@inject
async def create_book(
    book: Book,
    service: IBookService = Depends(Provide[Container.book_service]),
):
    return await service.add_book(Book(**book.model_dump()))

@router.put("/{book_id}", response_model=BookDTO)
@inject
async def update_book(
    book_id: int,
    data: Book,
    service: IBookService = Depends(Provide[Container.book_service]),
):
    updated = await service.update_book(book_id, data)
    if not updated:
        raise HTTPException(status_code=404, detail="Book not found")
    return updated


@router.delete("/{book_id}", status_code=204)
@inject
async def delete_book(
    book_id: int,
    service: IBookService = Depends(Provide[Container.book_service]),
):
    result = await service.delete_book(book_id)
    if not result:
        raise HTTPException(status_code=404, detail="Book not found")
    return None
