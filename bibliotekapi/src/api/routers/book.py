from typing import Iterable

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException

from src.container import Container
from src.infrastructure.services.ibook import IBookService
from src.infrastructure.dto.bookdto import BookDTO
from src.core.domain.book import Book

router = APIRouter()


@router.get("/", response_model=Iterable[BookDTO])
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


@router.post("/", response_model=BookDTO, status_code=201)
@inject
async def create_book(
    book: Book,
    service: IBookService = Depends(Provide[Container.book_service]),
):
    new_book = await service.add_book(book)
    return new_book


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
