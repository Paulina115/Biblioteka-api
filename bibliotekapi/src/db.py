"""A module providing database access"""

from __future__ import annotations

import asyncio
import uuid
from datetime import datetime, timedelta
from typing import List
from enum import Enum as sEnum

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import ForeignKey, String, Enum, ARRAY
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, AsyncAttrs, create_async_engine
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
)
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy.exc import OperationalError, DatabaseError
from asyncpg.exceptions import CannotConnectNowError, ConnectionDoesNotExistError

from src.config import config

class BookCopyStatus(sEnum):
    available = "available"
    reserved = "reserved"
    borrowed = "borrowed"

class HistoryStatus(sEnum):
    borrowed = "borrowed"
    returned = "returned"

class ReservationStatus(sEnum):
    active = "active"
    canceled = "canceled"
    collected = "collected"

class UserRole(sEnum):
    user = "user"
    librarian = "librarian"

class Base(AsyncAttrs, DeclarativeBase):
    pass

class Book(Base):
    __tablename__ = "book"

    book_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    isbn: Mapped[str | None] = mapped_column(unique=True)
    title: Mapped[str] = mapped_column(nullable=False)
    authors: Mapped[List[str]] = mapped_column(MutableList.as_mutable(ARRAY(String)),nullable=False)
    subject: Mapped[List[str]] = mapped_column(MutableList.as_mutable(ARRAY(String)),nullable=False)
    description: Mapped[str | None]
    publisher: Mapped[str | None] 
    publication_year: Mapped[int | None]
    language: Mapped[str] = mapped_column(default="pl", nullable=False)

    copies: Mapped[List[BookCopy]] = relationship("BookCopy", back_populates="book", cascade="all, delete-orphan")

class BookCopy(Base):
    __tablename__ = "book_copy"

    copy_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    book_id: Mapped[int] = mapped_column(ForeignKey("book.book_id"))
    status: Mapped[BookCopyStatus] = mapped_column(Enum(BookCopyStatus), default=BookCopyStatus.available, nullable=False)
    location: Mapped[str | None]

    book: Mapped[Book] = relationship("Book", back_populates="copies")
    histories: Mapped[List[History]] = relationship("History", back_populates="copy")
    reservations: Mapped[List[Reservation]] = relationship("Reservation", back_populates="copy")

class History(Base):
    __tablename__ = "history"

    history_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    copy_id: Mapped[int] = mapped_column(ForeignKey("book_copy.copy_id"))
    user_id: Mapped[UUID] = mapped_column(ForeignKey("user.user_id"))
    borrowed_date: Mapped[datetime] = mapped_column(default=lambda:datetime.now(), nullable=False)
    return_date: Mapped[datetime | None]
    due_date: Mapped[datetime] = mapped_column(default=lambda:datetime.now()+timedelta(days=14), nullable=False)
    status: Mapped[HistoryStatus] = mapped_column(Enum(HistoryStatus), default=HistoryStatus.borrowed, nullable=False)

    copy: Mapped[BookCopy] = relationship("BookCopy", back_populates="histories")
    user: Mapped[User] = relationship("User", back_populates="histories")

class Reservation(Base):
    __tablename__ = "reservation"

    reservation_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    copy_id: Mapped[int] = mapped_column(ForeignKey("book_copy.copy_id"))
    user_id: Mapped[UUID] = mapped_column(ForeignKey("user.user_id"))
    reservation_date: Mapped[datetime] = mapped_column(default=lambda:datetime.now(), nullable=False)
    expiration_date: Mapped[datetime] = mapped_column(default=lambda:datetime.now()+timedelta(days=3), nullable=False)
    status: Mapped[ReservationStatus] = mapped_column(Enum(ReservationStatus), default=ReservationStatus.active, nullable=False)
    
    copy: Mapped[BookCopy] = relationship("BookCopy", back_populates="reservations")
    user: Mapped[User] = relationship("User", back_populates="reservations")

class User(Base):
    __tablename__ = "user"

    user_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4)
    username: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    password: Mapped[str] = mapped_column(nullable=False) 
    role: Mapped[UserRole] = mapped_column(Enum(UserRole), default=UserRole.user)
    
    histories: Mapped[List[History]] = relationship("History", back_populates="user")
    reservations: Mapped[List[Reservation]] = relationship("Reservation", back_populates="user")


db_url = (
    f"postgresql+asyncpg://{config.DB_USER}:{config.DB_PASSWORD}"
    f"@{config.DB_HOST}/{config.DB_NAME}"
    )
engine = create_async_engine(db_url, echo=True, pool_pre_ping=True,)
# Create async session factory
async_session_factory = async_sessionmaker(
    engine,
    expire_on_commit=False,
)

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
                await conn.run_sync(Base.metadata.create_all)
            return
        except(
            OperationalError,
            DatabaseError,
            CannotConnectNowError,
            ConnectionDoesNotExistError
        ) as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            await asyncio.sleep(delay)
    raise ConnectionError("Could not connect to DB after several retries.")




