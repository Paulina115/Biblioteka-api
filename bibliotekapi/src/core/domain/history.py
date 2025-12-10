from dataclasses import dataclass
from datetime import datetime

@dataclass
class History:
    id: int | None
    user_id: int
    book_id: int
    borrowed_date: datetime
    due_date: datetime
    return_date: datetime | None
    status: str