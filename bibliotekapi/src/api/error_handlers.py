from fastapi import Request
from fastapi.responses import JSONResponse

from src.core.exceptions.exceptions import *

DOMAIN_EXCEPTION_MAPPING = {
    CopyNotFound: (404, "Copy not found"),
    UserNotFound: (404, "User not found"),
    BookNotFound: (404, "Book not found"),
    CopyNotAvailable: (409, "Copy is currently not available"),
    BookNotAvailable: (409, "Book is currently not available"),
    BookNotBorrowed: (409, "This copy is not borrowed"),
    EmailAlreadyExist: (409, "This email already exist"),
    BookBorrowed: (409, "One or more copy of this book is currently borrowed"),
    ISBNAlreadyExist: (409, "This isbn already exist")
}


async def domain_exception_handler(request: Request, exc: DomainError):
    status, message = DOMAIN_EXCEPTION_MAPPING.get(
        type(exc),
        (400, "Domain error")
    )

    return JSONResponse(
        status_code=status,
        content={"detail": message},
    )
