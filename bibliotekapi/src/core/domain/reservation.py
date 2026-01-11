"""Module containing reservation-related domain models."""

from enum import Enum
from pydantic import BaseModel, ConfigDict, Field, UUID4
from datetime import datetime, timedelta


class ReservationStatus(str, Enum):
    """
    Enum representing possible statuses of a book reservation.

    Attributes:
        active: The reservation is currently active.
        canceled: The reservation has been canceled by the user or system.
        collected: The reserved book was collected.
    """
    active = "active"
    canceled = "canceled"
    collected = "collected"

class ReservationCreate(BaseModel):
    """Model representing reservation's DTO attributes."""
    user_id: UUID4
    copy_id: int

class Reservation(ReservationCreate):
    """Model representing reservation's attributes in the database."""
    reservation_id: int | None = None
    reservation_date: datetime = Field(default_factory=lambda: datetime.now())
    expiration_date: datetime = Field(default_factory=lambda: datetime.now() + timedelta(days=3))
    status: ReservationStatus = ReservationStatus.active
  
    model_config = ConfigDict(from_attributes=True, extra="ignore")

    @property
    def is_expired(self) -> bool:
        """Method returns True if reservation is active and past expiration date"""
        return (
            self.status == ReservationStatus.active
            and self.expiration_date < datetime.now()
        )
