"""A module containing history DTO model."""

from pydantic import UUID4, BaseModel, ConfigDict
from datetime import datetime

from src.core.domain.history import HistoryStatus


class HistoryDTO(BaseModel):
    """A DTO model for history record."""  
    history_id: int
    copy_id: int
    user_id: UUID4
    borrowed_date: datetime
    due_date: datetime
    return_date: datetime | None
    status: HistoryStatus
    is_overdue: bool  

    @classmethod
    def from_domain(cls, history):
        return cls(
            history_id=history.history_id,
            copy_id=history.copy_id,
            user_id=history.user_id,
            borrowed_date=history.borrowed_date,
            due_date=history.due_date,
            return_date=history.return_date,
            status=history.status,
            is_overdue=history.is_overdue
        )
    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
    )