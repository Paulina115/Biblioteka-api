"""A DTO model for token details."""

from datetime import datetime
from pydantic import BaseModel, ConfigDict


class TokenDTO(BaseModel):
    """A DTO model for token details."""
    access_token: str
    token_type: str
    expires: datetime

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
    )