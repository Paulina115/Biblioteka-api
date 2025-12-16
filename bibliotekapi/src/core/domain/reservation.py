"""Module containing reservation-related domain models."""

from enum import Enum
from pydantic import BaseModel, ConfigDict
from datetime import datetime


class ReservationStatus(str, Enum):
    """
    Enum representing possible statuses of a book reservation.

    Attributes:
        active: The reservation is currently active.
        canceled: The reservation has been canceled by the user or system.
        expired: The reservation was not claimed in time and has expired.
    """
    active = "active"
    canceled = "canceled"
    expired = "expired"


class ReservationCreate(BaseModel):
    """Model representing reservation's DTO attributes."""
    user_id: int
    book_id: int


class Reservation(ReservationCreate):
    """Model representing history's attributes in the database."""
    id: int | None = None
    reservation_date: datetime
    expiration_date: datetime
    status: ReservationStatus

    model_config = ConfigDict(from_attributes=True, extra="ignore")
