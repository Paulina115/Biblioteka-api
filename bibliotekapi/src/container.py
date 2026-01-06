"""Module providing containers injecting dependencies."""

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Factory

# from src.infrastructure.repositories.user import UserRepository
from src.infrastructure.repositories.book import BookRepository
from src.infrastructure.repositories.book_copy import BookCopyRepository
# from src.infrastructure.repositories.history import HistoryRepository
# from src.infrastructure.repositories.reservation import ReservationRepository
from src.infrastructure.services.book import BookService
from src.infrastructure.services.book_copy import BookCopyService
# from src.infrastructure.services.history import HistoryService
# from src.infrastructure.services.reservation import ReservationService
# from src.infrastructure.services.user import UserService
from src.db import async_session_factory


class Container(DeclarativeContainer):
    """Container class for dependency injecting purposes."""
    book_repository = Factory(
        BookRepository,
        sessionmaker= lambda: async_session_factory()
        )
    book_copy_repository = Factory(
        BookCopyRepository,
        sessionmaker= lambda: async_session_factory()
        )
    # history_repository = Factory(
    #     HistoryRepository,
    #     sessionmaker= lambda: async_session_factory()
    #     )
    # reservation_repository = Factory(
    #     ReservationRepository,
    #     sessionmaker= lambda: async_session_factory()
    #     )
    # user_repository = Factory(
    #     UserRepository,
    #     sessionmaker= lambda: async_session_factory()
    # )

    book_service = Factory(
        BookService,
        repository=book_repository,
    )

    book_copy_service = Factory(
        BookCopyService,
        repository=book_copy_repository,
    )

    # history_service = Factory(
    #     HistoryService,
    #     repository=history_repository,
    # )
    # reservation_service = Factory(
    #     ReservationService,
    #     repository=reservation_repository,
    #     book_copy_repo=book_copy_repository,
    #     history_repo = history_repository,

    # )
    # user_service = Factory(
    #     UserService,
    #     repository=user_repository,
    # )
   