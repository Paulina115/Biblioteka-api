import asyncio

import databases
import sqlalchemy
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.exc import OperationalError, DatabaseError
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.mutable import MutableList
from asyncpg.exceptions import (    # type: ignore
    CannotConnectNowError,
    ConnectionDoesNotExistError,
)

from src.config import config

metadata = sqlalchemy.MetaData()

book_table = sqlalchemy.Table(
    "books",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("title", sqlalchemy.String,nullable=False),
    sqlalchemy.Column("author", sqlalchemy.String, nullable=False),
    sqlalchemy.Column("description", sqlalchemy.String),
    sqlalchemy.Column("category", sqlalchemy.String),
    sqlalchemy.Column("isbn", sqlalchemy.String, unique=True),
    sqlalchemy.Column("publication_year", sqlalchemy.Integer),
    sqlalchemy.Column("available", sqlalchemy.Boolean, default=True),
    
    )

history_table = sqlalchemy.Table(
    "history",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("borrowed_date", sqlalchemy.DateTime),
    sqlalchemy.Column("due_date", sqlalchemy.DateTime),
    sqlalchemy.Column("return_date", sqlalchemy.DateTime),
    sqlalchemy.Column("status", sqlalchemy.String),
    sqlalchemy.Column("user_id", sqlalchemy.ForeignKey("books.id"), nullable=False,),
    sqlalchemy.Column("book_id", sqlalchemy.ForeignKey("books.id"),nullable=False,),

)

reservation_table = sqlalchemy.Table(
    "reservation",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("reservation_date", sqlalchemy.DateTime),
    sqlalchemy.Column("expiration_date", sqlalchemy.DateTime),
    sqlalchemy.Column("status", sqlalchemy.String),
    sqlalchemy.Column("user_id", sqlalchemy.ForeignKey("users.id"), nullable=False,),
    sqlalchemy.Column("book_id", sqlalchemy.ForeignKey("books.id"),nullable=False,),
)

user_table = sqlalchemy.Table(
    "users",
    metadata,
    sqlalchemy.Column(
        "id",
        UUID(as_uuid=True),
        primary_key=True,
        server_default=sqlalchemy.text("gen_random_uuid()"),
    ),
    sqlalchemy.Column("email", sqlalchemy.String, unique=True),
    sqlalchemy.Column("password", sqlalchemy.String),
)

db_uri = (
    f"postgresql+asyncpg://{config.DB_USER}:{config.DB_PASSWORD}"
    f"@{config.DB_HOST}/{config.DB_NAME}"
)

engine = create_async_engine(
    db_uri,
    echo=True,
    future=True,
    pool_pre_ping=True,
)

database = databases.Database(db_uri)


async def init_db(retries: int = 5, delay: int = 5) -> None:
    """Function initializing the DB.

    Args:
        retries (int, optional): Number of retries of connect to DB.
            Defaults to 5.
        delay (int, optional): Delay of connect do DB. Defaults to 2.
    """
    for attempt in range(retries):
        try:
            async with engine.begin() as conn:
                await conn.run_sync(metadata.create_all)
            return
        except (
            OperationalError,
            DatabaseError,
            CannotConnectNowError,
            ConnectionDoesNotExistError,
        ) as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            await asyncio.sleep(delay)

    raise ConnectionError("Could not connect to DB after several retries.")