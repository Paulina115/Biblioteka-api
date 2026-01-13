"""Module providing containers injecting dependencies."""

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Factory


from src.infrastructure.services.book import BookService
from src.infrastructure.services.book_copy import BookCopyService
from src.infrastructure.services.history import HistoryService
from src.infrastructure.services.reservation import ReservationService
from src.infrastructure.services.user import UserService
from src.infrastructure.services.unit_of_work import UnitOfWork

class Container(DeclarativeContainer):
    """Conntainer class for dependency injecting purposes."""

    unit_of_work = Factory(UnitOfWork)

    book_service = Factory(
        BookService,
        uow=unit_of_work,
    )

    book_copy_service = Factory(
        BookCopyService,
        uow=unit_of_work,
    )

    history_service = Factory(
        HistoryService,
        uow=unit_of_work,
    )

    reservation_service = Factory(
        ReservationService,
        uow=unit_of_work,
    )

    user_service = Factory(
        UserService,
        uow=unit_of_work,
    )
