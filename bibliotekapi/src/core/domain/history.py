"""Module containing history-related domain models."""

from enum import Enum
from pydantic import BaseModel, ConfigDict
from datetime import datetime


class HistoryStatus(str, Enum):
    """
    Enum representing possible statuses of a book borrowing record.

    Attributes:
        borrowed: The book has been borrowed and is currently within the allowed return period.
        returned: The book has been returned.
        overdue: The book has not been returned by the due date and is overdue.
    """
    borrowed = "borrowed"
    returned = "returned"
    overdue = "overdue"


class HistoryCreate(BaseModel):
    """Model representing history's DTO attributes."""
    user_id: int
    book_copy_id: int


class History(HistoryCreate):
    """Model representing history's attributes in the database."""
    history_id: int | None = None
    borrowed_date: datetime
    due_date: datetime
    return_date: datetime | None
    status: HistoryStatus = HistoryStatus.borrowed

    model_config = ConfigDict(from_attributes=True, extra="ignore")
    
