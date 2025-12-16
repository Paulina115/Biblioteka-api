from pydantic import BaseModel, ConfigDict

from src.core.domain.book import Book

class BookDTO(BaseModel):
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
    

