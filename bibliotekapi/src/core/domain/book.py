"""Module containing book-related domain models."""

from pydantic import BaseModel, ConfigDict, Field


class BookCreate(BaseModel):
    """Model representing book's DTO attributes."""
    isbn: str | None = None
    title: str
    authors: list[str] = Field(default_factory=list)
    subject: list[str] = Field(default_factory=list)
    description: str | None = None
    publisher: str | None = None
    publication_year: int | None = None
    language: str = "pl"


class Book(BookCreate):
    """Model representing book's attributes in the database."""
    book_id: int | None = None

    model_config = ConfigDict(from_attributes=True, extra="ignore")


