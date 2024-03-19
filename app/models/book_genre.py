from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from ..db import db

class BookGenre(db.Model):
    __tablename__ = "book_genre"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    book_id: Mapped[int] = mapped_column(ForeignKey("book.id"), nullable=True)
    genre_id: Mapped[int] = mapped_column(ForeignKey("genre.id"), nullable=True)
