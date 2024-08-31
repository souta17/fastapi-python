from sqlmodel import SQLModel, Field, Column, Relationship
import sqlalchemy.dialects.postgresql as pg
import uuid
from typing import Optional, List
from datetime import datetime, date


class User(SQLModel, table=True):
    __tablename__ = 'users'
    uid: uuid.UUID = Field(sa_column=Column(
        pg.UUID, nullable=False, primary_key=True, default=uuid.uuid4,))
    username: str
    first_name: str
    last_name: str
    email: str
    is_verified: bool = Field(default=False)
    password_hash: str = Field(exclude=True)
    created_at: datetime = Field(
        sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    updated_at: datetime = Field(
        sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    books: List["Book"] = Relationship(
        back_populates="user", sa_relationship_kwargs={"lazy": "selectin"})

    def __repr__(self):
        return f"<User {self.username}>"


class Book(SQLModel, table=True):
    __tablename__ = "books"
    uid: uuid.UUID = Field(sa_column=Column(
        pg.UUID,
        nullable=False,
        primary_key=True,
        default=uuid.uuid4)
    )
    title: str
    author: str
    publisher: str
    published_date: date
    pagecount: int
    language: str
    user_uid: Optional[uuid.uuid4] = Field(
        default=None, foreign_key="users.uid")
    created_at: datetime = Field(sa_column=Column(
        pg.TIMESTAMP,
        default=datetime.now)
    )
    updated_at: datetime = Field(sa_column=Column(
        pg.TIMESTAMP,
        default=datetime.now)
    )
    user: Optional[User] = Relationship(back_populates="books")

    def __repr__(self) -> str:
        return f"<Book {self.title}>"
