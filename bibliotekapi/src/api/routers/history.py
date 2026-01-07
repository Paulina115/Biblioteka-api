"""A module containing history routers"""

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException

from src.container import Container
from src.infrastructure.services.ibook_copy import IBookCopyService
from src.core.domain.book_copy import BookCopy, BookCopyCreate, BookCopyStatus

router = APIRouter()