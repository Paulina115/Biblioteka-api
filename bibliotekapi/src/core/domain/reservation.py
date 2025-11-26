from dataclasses import dataclass
from datetime import datetime

@dataclass
class Reservation:
    id: int
    user_id: int
    book_id: int
    reservation_date: datetime
    expiration_date: datetime
    status: str
