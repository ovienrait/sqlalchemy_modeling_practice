from datetime import datetime
from typing import List, Optional

from sqlalchemy import DateTime, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    """Базовый класс для всех моделей SQLAlchemy."""

    pass


class Genre(Base):
    """Модель для хранения информации о жанрах книг."""

    __tablename__ = 'genre'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False, unique=True)

    books: Mapped[List['Book']] = relationship(
        back_populates='genre', cascade='all, delete-orphan'
    )


class Author(Base):
    """Модель для хранения информации об авторах книг."""

    __tablename__ = 'author'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)

    books: Mapped[List['Book']] = relationship(
        back_populates='author', cascade='all, delete-orphan'
    )


class City(Base):
    """Модель для хранения информации о городах."""

    __tablename__ = 'city'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    days_delivery: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    clients: Mapped[List['Client']] = relationship(
        back_populates='city', cascade='all, delete-orphan'
    )


class Book(Base):
    """Модель для хранения информации о книгах."""

    __tablename__ = 'book'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    price: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    amount: Mapped[int] = mapped_column(Integer, nullable=False)
    genre_id: Mapped[int] = mapped_column(
        ForeignKey('genre.id'), nullable=False
    )
    author_id: Mapped[int] = mapped_column(
        ForeignKey('author.id'), nullable=False
    )

    genre: Mapped['Genre'] = relationship(back_populates='books')
    author: Mapped['Author'] = relationship(back_populates='books')
    buy_books: Mapped[List['BuyBook']] = relationship(
        back_populates='book', cascade='all, delete-orphan'
    )


class Client(Base):
    """Модель для хранения информации о клиентах."""

    __tablename__ = 'client'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    city_id: Mapped[int] = mapped_column(ForeignKey('city.id'), nullable=False)

    city: Mapped['City'] = relationship(back_populates='clients')
    buys: Mapped[List['Buy']] = relationship(
        back_populates='client', cascade='all, delete-orphan'
    )


class Buy(Base):
    """Модель для хранения информации о покупках."""

    __tablename__ = 'buy'

    id: Mapped[int] = mapped_column(primary_key=True)
    description: Mapped[Optional[str]] = mapped_column(Text)
    client_id: Mapped[int] = mapped_column(
        ForeignKey('client.id'), nullable=False
    )

    client: Mapped['Client'] = relationship(back_populates='buys')
    buy_books: Mapped[List['BuyBook']] = relationship(
        back_populates='buy', cascade='all, delete-orphan'
    )
    buy_steps: Mapped[List['BuyStep']] = relationship(
        back_populates='buy', cascade='all, delete-orphan'
    )


class Step(Base):
    """Модель для хранения информации о шагах."""

    __tablename__ = 'step'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)

    buy_steps: Mapped[List['BuyStep']] = relationship(
        back_populates='step', cascade='all, delete-orphan'
    )


class BuyBook(Base):
    """Модель для хранения информации о книгах в покупке."""

    __tablename__ = 'buy_book'

    id: Mapped[int] = mapped_column(primary_key=True)
    amount: Mapped[int] = mapped_column(Integer, nullable=False)
    buy_id: Mapped[int] = mapped_column(ForeignKey('buy.id'), nullable=False)
    book_id: Mapped[int] = mapped_column(ForeignKey('book.id'), nullable=False)

    buy: Mapped['Buy'] = relationship(back_populates='buy_books')
    book: Mapped['Book'] = relationship(back_populates='buy_books')


class BuyStep(Base):
    """Модель для хранения информации о шагах покупки."""

    __tablename__ = 'buy_step'

    id: Mapped[int] = mapped_column(primary_key=True)
    step_beg: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    step_end: Mapped[Optional[datetime]] = mapped_column(DateTime)
    buy_id: Mapped[int] = mapped_column(ForeignKey('buy.id'), nullable=False)
    step_id: Mapped[int] = mapped_column(ForeignKey('step.id'), nullable=False)

    buy: Mapped['Buy'] = relationship(back_populates='buy_steps')
    step: Mapped['Step'] = relationship(back_populates='buy_steps')
