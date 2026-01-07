"""A module containing reservation DTO model."""

from pydantic import UUID4, BaseModel, ConfigDict
from datetime import datetime

from src.core.domain.reservation import ReservationStatus


class ReservationDTO(BaseModel):
    """A DTO model for reservation record."""
    reservation_id: int
    copy_id: int
    user_id: UUID4
    reservation_date: datetime
    expiration_date: datetime
    status: ReservationStatus
    is_expired: bool

    @classmethod
    def from_domain(cls, reservation):
        return cls(
            reservation_id=reservation.reservation_id,
            copy_id=reservation.copy_id,
            user_id=reservation.user_id,
            reservation_date=reservation.reservation_date,
            expiration_date=reservation.expiration_date,
            status=reservation.status,
            is_expired=reservation.is_expired
        )
    
    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
    )