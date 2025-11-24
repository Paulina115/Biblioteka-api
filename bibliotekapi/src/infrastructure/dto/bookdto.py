from pydantic import BaseModel, ConfigDict

from core.domain.book import Book, Category

class BookDTO(BaseModel):
    id: int
    title: str
    author: str
    description: str
    category: Category
    isbn: str
    publication_year: str
    available: bool

    model_config = ConfigDict(
        from_atributes=True,
        extra="ignore",
        arbitrary_types_allowed=True,
    )
    

