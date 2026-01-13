"""Module containing history related domain models."""

from enum import Enum
from pydantic import BaseModel, ConfigDict, Field, UUID4
from datetime import datetime, timedelta


class HistoryStatus(str, Enum):
    """
    Enum representing possible statuses of a book borrowing record.

    Attributes:
        borrowed: The book has been borrowed.
        returned: The book has been returned.
    """
    borrowed = "borrowed"
    returned = "returned"

class HistoryCreate(BaseModel):
    """Model representing history's DTO attributes."""
    user_id: UUID4
    copy_id: int
    
class History(HistoryCreate):
    """Model representing history's attributes in the database."""
    history_id: int | None = None
    borrowed_date: datetime = Field(default_factory=lambda: datetime.now())
    due_date: datetime = Field(default_factory=lambda: datetime.now() + timedelta(days=14))
    return_date: datetime | None = None
    status: HistoryStatus = HistoryStatus.borrowed
    
    model_config = ConfigDict(from_attributes=True, extra="ignore")
    
    @property
    def is_overdue(self) -> bool:
        """Method returns True if the book is borrowed and past due date"""
        return (
            self.status == HistoryStatus.borrowed
            and self.return_date is None
            and self.due_date < datetime.now()
        )
