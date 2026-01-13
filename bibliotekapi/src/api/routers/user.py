"""A module containing user routers"""

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException, Body
from pydantic import UUID4, EmailStr
from fastapi.security import OAuth2PasswordRequestForm


from src.container import Container
from src.infrastructure.services.iuser import IUserService
from src.core.domain.user import UserCreate, UserRole, UserLogin, User
from src.infrastructure.dto.userdto import UserDTO
from src.infrastructure.dto.tokendto import TokenDTO
from src.infrastructure.auth.auth import librarian_required, get_current_user


router = APIRouter()

@router.get("/all", response_model=list[UserDTO])
@inject
async def get_all_users(
    service: IUserService = Depends(Provide[Container.user_service]),
    # current_user: UserDTO = Depends(librarian_required)
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
) -> dict:
    """The endpoint for registering a new user.
    
    Args:
        data (UserCreate): The attributes of the user.
        service (IHistoryService): The injected service dependency.
    
    Returns:
        dict: The newly registered user.
    """
    user = await service.register_user(data)
    if user:
        return user.model_dump()
    raise HTTPException(status_code=404, detail="User not found.")

@router.patch("/update/username", response_model=UserDTO)
@inject
async def update_user_username(
    username: str,
    service: IUserService = Depends(Provide[Container.user_service]),
    current_user: UserDTO = Depends(get_current_user)
) -> dict:
    """The endpoint for updating user username.
    
    Args:
        username (str): The new user username.
        service (IUserService): The injected service dependency.
        current_user (UserDTO): The injected user authentication dependency.

    Returns:
        dict: The updated user record.
    """
    user_id = current_user.user_id
    user = await service.update_user_username(user_id, username)
    if user:
        return user.model_dump()
    raise HTTPException(status_code=404, detail="User not found")

@router.patch("/update/email", response_model=UserDTO)
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

@router.patch("/update/password", response_model=UserDTO)
@inject
async def change_user_password(
    data: dict = Body(..., example={"password": "newpassword"}),
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
    user = await service.change_user_password(user_id, data["password"])
    return user.model_dump()
    if user:
        return user.model_dump()
    raise HTTPException(status_code=404, detail="User not found")

@router.patch("/set_role", response_model=UserDTO)
@inject
async def set_user_role(
    user_id: UUID4,
    role: UserRole,
    service: IUserService = Depends(Provide[Container.user_service]),
) -> dict:
    """The endpoint for setting user role.
    
    Args:
        user_id (UUID4): The user id.
        role (UserRole): The user role to set.
        service (IUserService): The injected service dependency.

    Returns:
        dict: The updated user record.
    """
    user = await service.set_role(user_id, role)
    if user:
        return user.model_dump()
    raise HTTPException(status_code=404, detail="User not found")

from fastapi.security import OAuth2PasswordRequestForm

@router.post("/login", response_model=TokenDTO)
@inject
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    service: IUserService = Depends(Provide[Container.user_service])
):
    """The endpoint for authenticate user.
    
    Args:
        form data (OAuth2PasswordRequestForm): The user login data.
        service (IUserService): The injected service dependency.

    Returns:
        dict: The updated user record.
    """
    user_login = UserLogin(email=form_data.username, password=form_data.password)
    token_details = await service.authenticate_user(user_login)
    if token_details:
        return token_details.model_dump()
    raise HTTPException(status_code=401, detail="Invalid credentials")



    
