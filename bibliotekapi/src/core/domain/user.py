"""A model containing user-related models."""

from enum import Enum
from pydantic import BaseModel, ConfigDict, EmailStr
from uuid import UUID, uuid4


class UserRole(str, Enum):
    """
    Enum representing possible roles of a user in the library system.

    Attributes:
        user: Standard library user, can view books and reserve them.
        librarian: Can manage books (add, delete) and view all histories.
        admin: Full access, including managing users.
    """
    user = "user"
    librarian = "librarian"
    admin = "admin"


class UserCreate(BaseModel):
    """Model for creating a new user."""
    username: str
    email: EmailStr
    password: str 
    membership_number: str | None = None
    role: UserRole.user


class User(UserCreate):
    """User model representing a user in the database."""
    id: UUID = uuid4()

    model_config = ConfigDict(from_attributes=True, extra="ignore")


