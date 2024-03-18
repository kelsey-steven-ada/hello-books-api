from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from ..db import db

class Book(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    description: Mapped[str]
    author_id: Mapped[int] = mapped_column(ForeignKey("author.id"), nullable=True)
    author: Mapped["Author"] = relationship(back_populates="books")

    def to_dict(self):
        book_as_dict = {}
        book_as_dict["id"] = self.id
        book_as_dict["title"] = self.title
        book_as_dict["description"] = self.description

        if self.author:
            book_as_dict["author"] = self.author.name

        return book_as_dict
    
    @classmethod
    def from_dict(cls, book_data):
        author_id = book_data.get("author_id")
        new_book = Book(
            title=book_data["title"],
            description=book_data["description"],
            author_id=author_id
        )

        return new_book