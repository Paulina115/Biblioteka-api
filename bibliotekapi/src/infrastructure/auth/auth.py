"""Module containing user authentication methods."""

from fastapi import Depends, HTTPException
from jose import jwt, JWTError
from dependency_injector.wiring import inject, Provide
from src.container import Container
from src.infrastructure.services.iuser import IUserService
from src.core.domain.user import UserRole
from src.infrastructure.dto.userdto import UserDTO
from src.infrastructure.utils.consts import SECRET_KEY, ALGORITHM
from fastapi.security import OAuth2PasswordBearer
from uuid import UUID

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/login")

@inject
async def get_current_user(
    token: str = Depends(oauth2_scheme),
    service: IUserService = Depends(Provide[Container.user_service])
) -> UserDTO :
    """Method returning current user based on token.

    Args:
        token (str): The user token.
        service (IUserService): The injected service dependency.

    Returns:
        UserDTO: The current user data.
    """
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    user_id = UUID(payload["sub"])
    user = await service.get_user_by_uuid(user_id)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user

async def librarian_required(current_user: UserDTO = Depends(get_current_user)) -> UserDTO:
    """Method checking if current user is librarian.

    Args:
        current_user (UserDTO): The injected current user dependency.

    Returns:
        UserDTO: The current user data.
    """

    if current_user.role != UserRole.librarian:
        raise HTTPException(status_code=403, detail="Librarian role required")
    return current_user
