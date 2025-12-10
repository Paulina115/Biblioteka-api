from typing import Iterable

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException

from src.container import Container
from src.infrastructure.services.iuser import IUserService
from src.infrastructure.dto.userdto import UserDTO
from src.core.domain.user import User

# router = APIRouter()

# @router.get("/all", response_model=Iterable[UserDTO])
# @inject
# async def get_all_users(
#     service: IUserService = Depends(Provide[Container.user_service]),
# ):
#     users = await service.get_all_users()
#     return users
