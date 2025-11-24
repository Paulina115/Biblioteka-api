from dataclasses import dataclass

@dataclass

class History:
    id: int
    user_id: int
    book_id: int
    reservation_date: str
    status: str