from pydantic import BaseModel, ConfigDict

from core.domain.book import Book

class BookDTO(BaseModel):
    id: int
    title: str
    author: str
    description: str
    category: str
    isbn: str
    publication_year: str
    available: bool

    model_config = ConfigDict(
        from_atributes=True,
        extra="ignore",
    )
    

