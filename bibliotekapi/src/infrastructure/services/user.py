# from typing import Iterable

# from src.core.domain.user import User
# from src.core.repositories.iuser import IUserRepository
# from src.infrastructure.services.iuser import IUserService

# class UserService(IUserService):

#     _repository: IUserRepository

#     def __init__(self, repository: IUserRepository):
#         self._repository = repository

#     async def get_all_users(self) -> Iterable[User]:
#        return await self._repository.get_all_users()

#     async def get_user_by_id(self, id: int) -> User:
#         return await self._repository.get_user_by_id(id)

#     async def get_user_by_email(self, email: str) -> User:
#         return await self._repository.get_user_by_email(email)

#     async def create_user(self, data: User) -> None:
#         return await self._repository.create_user(data)

#     async def delete_user(self, id: int) -> None:
#         return await self._repository.delete_user(id)