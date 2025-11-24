from dataclasses import dataclass

@dataclass
class Reservation:
    id: int
    user_id: int
    book_id: int
    reservation_date: str
    status: str
