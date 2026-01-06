# from typing import Any, Iterable

# from asyncpg import Record  # type: ignore
# from sqlalchemy import select,join

# from src.core.repositories.iuser import IUserRepository
# from src.core.domain.user import User

# from src.db import (
#     user_table,
#     database,
# )
# from src.infrastructure.dto.userdto import UserDTO

# class UserRepository(IUserRepository):

#     async def get_all_users(self) -> Iterable[User]:
#         query = (
#             select(user_table)
#         )
#         users = await database.fetch_all(query)

#         return [UserDTO.from_record(user) for user in users]

#     async def get_user_by_id(self, id: int) -> User:
#         query = ( 
#             select(user_table).where(user_table.id == id)
#         )
#         user = await database.fetch_one(query)
        
#         return UserDTO.from_record(user) if user else None

#     async def get_user_by_email(self, email: str) -> User:
#         query = ( 
#             select(user_table).where(user_table.email == email)
#         )
#         user = await database.fetch_one(query)
        
#         return UserDTO.from_record(user) if user else None

#     async def create_user(self, data: User) -> None:
#         query = (
#             user_table.insert().values(**data.model_dump())
#         )
#         new_user_id = await database.execute(query)
#         new_user = await self.get_user_by_id(new_user_id)

#         return User(**dict(new_user)) if new_user else None

#     async def delete_user(self, id: int) -> None:
#        if self._get_user_by_id(id):
#             query = ( user_table
#             .delete()
#             .where(user_table.c.id == id)
#             )
#             await database.execute(query)
#             return True 
#        return False
    
#     async def _get_user_by_id(self, id: int) -> Record | None: # type: ignore
#             query = (
#                 user_table.select()
#                 .where(user_table.c.id == id)
#             )

#             return await database.fetch_one(query)