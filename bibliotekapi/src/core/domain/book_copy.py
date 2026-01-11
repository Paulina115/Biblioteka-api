"""Module containing book copy related domain model"""

from enum import Enum
from pydantic import BaseModel, ConfigDict


class BookCopyStatus(str, Enum):
    """Enum representing possible statuses of a book copy.
    
        Attributes:
            available: The copy is available and can be borrowed.
            reserved: The copy is currently reserved.
            borrowed: The copy is currently borrowed.
    """
    available = "available"
    reserved = "reserved"
    borrowed = "borrowed"

class BookCopyCreate(BaseModel):
    """Model representing book copy's DTO attributes"""
    book_id: int
    location: str | None = None

class BookCopy(BookCopyCreate):
    """"Model representing book copy's attributes in database"""
    copy_id: int | None = None
    status: BookCopyStatus = BookCopyStatus.available

    model_config = ConfigDict(from_attributes=True, extra="ignore")

class BookCopyUpdate(BaseModel):
    """Model for updating a book copy"""
    location: str | None = None

    model_config = ConfigDict(from_attributes=True, extra="ignore")