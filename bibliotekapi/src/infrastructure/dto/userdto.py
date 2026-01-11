"""A module containing user DTO model."""

from pydantic import UUID4, BaseModel, EmailStr, ConfigDict

from src.core.domain.user import UserRole


class UserDTO(BaseModel):
    """A DTO model for user."""
    user_id: UUID4
    username: str
    email: EmailStr
    membership_number: str | None = None
    role: UserRole = UserRole.user

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
    )