"""A module containing user routers"""

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException
from pydantic import UUID4, EmailStr

from src.container import Container
from src.infrastructure.services.iuser import IUserService
from src.core.domain.user import UserCreate
from src.infrastructure.dto.userdto import UserDTO
from src.infrastructure.dto.tokendto import TokenDTO
from src.infrastructure.auth.auth import librarian_required, get_current_user


router = APIRouter()

@router.get("/all", response_model=list[UserDTO])
@inject
async def get_all_users(
    service: IUserService = Depends(Provide[Container.user_service]),
    current_user: UserDTO = Depends(librarian_required)
) -> list:
    """The endpoint for getting all users from the repository (Intended for Librarian use).

    Args:
        service (IHistoryService): The injected service dependency.
        current_user (UserDTO): The injected user authentication dependency.

    Returns:
        list: The collection of the all users.
    """
    users = await service.get_all_users()
    return users

@router.get("/userid", response_model=UserDTO)
@inject
async def get_user_by_uuid(
    user_id: UUID4,
    service: IUserService = Depends(Provide[Container.user_service]),
    current_user: UserDTO = Depends(librarian_required)
) -> dict:
    """The endpoint for getting a user from the repository.(Intended for Librarian use).

    Args:
        user_id (UUID4): The id of the user.
        service (IHistoryService): The injected service dependency.
        current_user (UserDTO): The injected user authentication dependency.

    Returns:
        dict: The user data if exists.
    """
    user = await service.get_user_by_uuid(user_id)
    if user:
        return user.model_dump()
    raise HTTPException(status_code=404, detail="User not found")

@router.get("/email", response_model=UserDTO)
@inject
async def get_user_by_email(
    email: EmailStr,
    service: IUserService = Depends(Provide[Container.user_service]),
    current_user: UserDTO = Depends(librarian_required)
) -> dict:
    """The endpoint for  getting a user by email from the repository. (Intended for Librarian use).

    Args:
        email (EmailStr): The email of the user.
        service (IHistoryService): The injected service dependency.
        current_user (UserDTO): The injected user authentication dependency.
    
    Returns:
        dict: The user data if exists.
    """
    user = await service.get_user_by_email(email)
    if user:
        return user.model_dump()
    raise HTTPException(status_code=404, detail="User not found")

@router.get("/username", response_model=UserDTO)
@inject
async def get_user_by_username(
    username: str,
    service: IUserService = Depends(Provide[Container.user_service]),
    current_user: UserDTO = Depends(librarian_required)
) -> list:
    """The endpoint for getting a user by username from the repository. (Intended for Librarian use).

    Args:
        username (str): The username of the user.
        service (IHistoryService): The injected service dependency.
        current_user (UserDTO): The injected user authentication dependency.
    
    Returns:
        list: The collection of user data.
    """
    users = await service.get_user_by_username(username)
    return users

@router.post("/register", response_model=UserDTO, status_code=201)
@inject
async def register_user(
    data: UserCreate,
    service: IUserService = Depends(Provide[Container.user_service]),
    current_user: UserDTO = Depends(librarian_required)
) -> dict:
    """The endpoint for registering a new user.
    
    Args:
        data (UserCreate): The attributes of the user.
        service (IHistoryService): The injected service dependency.
        current_user (UserDTO): The injected user authentication dependency.
    
    Returns:
        dict: The newly registered user.
    """

@router.put("/update", response_model=UserDTO)
@inject
async def update_user_email(
    new_email: EmailStr,
    service: IUserService = Depends(Provide[Container.user_service]),
    current_user: UserDTO = Depends(get_current_user)
) -> dict:
    """The endpoint for updating user email.
    
    Args:
        new_email (EmailStr): The new user email.
        service (IUserService): The injected service dependency.
        current_user (UserDTO): The injected user authentication dependency.

    Returns:
        dict: The updated user record.
    """
    user_id = current_user.user_id
    user = await service.update_user_email(user_id, new_email)
    if user:
        return user.model_dump()
    raise HTTPException(status_code=404, detail="User not found")

@router.put("/update", response_model=UserDTO)
@inject
async def change_user_password(
    new_password: str,
    service: IUserService = Depends(Provide[Container.user_service]),
    current_user: UserDTO = Depends(get_current_user)
) -> dict:
    """The enpoint for changing user password.
    
    Args:
        new password (str): The new user password.
        service (IUserService): The injected service dependency.
        current_user (UserDTO): The injected user authentication dependency.

    Returns:
        dict: The updated user record.
    """
    user_id = current_user.user_id
    user = await service.change_user_password(user_id, new_password)
    if user:
        return user.model_dump()
    raise HTTPException(status_code=404, detail="User not found")

@router.post("/token", response_model=TokenDTO, status_code=200)
@inject
async def authenticate_user(
    user: UserCreate,
    service: IUserService = Depends(Provide[Container.user_service]),
) -> TokenDTO | None:
    """The endpoint for  authenticating the user.

    Args:
        user (UserCreate): The user data.
        service (IUserService): The injected service dependency.
    
    Returns:
        TokenDTO | None: The token details.
    """
    if token_details := await service.authenticate_user(user):
        print("user confirmed")
        return token_details.model_dump()

    raise HTTPException(
        status_code=401,
        detail="Provided incorrect credentials",
    )


    
