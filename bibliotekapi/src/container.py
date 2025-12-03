"""Module providing containers injecting dependencies."""

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Factory, Singleton

from src.infrastructure.repositories.user import UserRepository
from src.infrastructure.repositories.book import BookRepository
from src.infrastructure.repositories.history import HistoryRepository
from src.infrastructure.repositories.reservation import ReservationRepository
from src.infrastructure.services.book import BookService
from src.infrastructure.services.history import HistoryService
from src.infrastructure.services.reservation import ReservationService
from src.infrastructure.services.user import UserService


class Container(DeclarativeContainer):
    """Container class for dependency injecting purposes."""
    book_repository = Singleton(BookRepository)
    history_repository = Singleton(HistoryRepository)
    reservation_repository = Singleton(ReservationRepository)
    user_repository = Singleton(UserRepository)

    book_service = Factory(
        BookService,
        repository=book_repository,
    )
    history_service = Factory(
        HistoryService,
        repository=history_repository,
    )
    reservation_service = Factory(
        ReservationService,
        repository=reservation_repository,
        book_repo=book_repository,
        history_repo = history_repository,

    )
    user_service = Factory(
        UserService,
        repository=user_repository,
    )