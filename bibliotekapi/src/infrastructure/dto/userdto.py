from pydantic import BaseModel, ConfigDict

from src.core.domain.user import User


class UserDTO(BaseModel):
    id: int
    name: str
    email: str

    model_config = ConfigDict(
        from_atributes=True,
        extra="ignore",
    )
    