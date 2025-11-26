from dataclasses import dataclass

@dataclass
class Book:
    id: int
    title: str
    author: str
    description: str
    category: str
    isbn: str
    publication_year: int
    available: bool
    

