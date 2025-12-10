from pydantic import BaseModel, ConfigDict

from src.core.domain.history import History


class HistoryDTO(BaseModel):
    id: int
    user_id: int
    book_id: int
    reservation_date: str
    status: str

    model_config = ConfigDict(
        from_atributes=True,
        extra="ignore",
    )
    