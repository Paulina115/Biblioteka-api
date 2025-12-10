from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.exception_handlers import http_exception_handler

from src.api.routers.book import router as book_router
from src.api.routers.history import router as history_router
from src.api.routers.reservation import router as reservation_router
# from src.api.routers.user import router as user_router
from src.container import Container
from src.db import database, init_db

container = Container()
container.wire(modules=[
    "src.api.routers.book",
    "src.api.routers.history",
    "src.api.routers.reservation",
    # "src.api.routers.user",
])


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncGenerator:
    """Lifespan function working on app startup."""
    await init_db()
    await database.connect()
    yield
    await database.disconnect()


app = FastAPI(lifespan=lifespan)
app.include_router(book_router, prefix="/book")
app.include_router(history_router, prefix="/history")
app.include_router(reservation_router, prefix="/reservation")
# app.include_router(user_router, prefix="")


@app.exception_handler(HTTPException)
async def http_exception_handle_logging(
    request: Request,
    exception: HTTPException,
) -> Response:
    """A function handling http exceptions for logging purposes.

    Args:
        request (Request): The incoming HTTP request.
        exception (HTTPException): A related exception.

    Returns:
        Response: The HTTP response.
    """
    return await http_exception_handler(request, exception)