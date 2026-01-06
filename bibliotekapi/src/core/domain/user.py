"""A model containing user-related models."""

from enum import Enum
from pydantic import BaseModel, ConfigDict, EmailStr, Field
from uuid import UUID, uuid4


class UserRole(str, Enum):
    """
    Enum representing possible roles of a user in the library system.

    Attributes:
        user: Standard library user, can view books and reserve them.
        librarian: Can manage books (add, delete) and view all histories.
    """
    user = "user"
    librarian = "librarian"


class UserCreate(BaseModel):
    """Model for creating a new user."""
    username: str
    email: EmailStr
    password: str 
    role: UserRole = UserRole.user


class User(UserCreate):
    """User model representing a user in the database."""
    user_id: UUID = Field(default_factory=uuid4)

    model_config = ConfigDict(from_attributes=True, extra="ignore")



