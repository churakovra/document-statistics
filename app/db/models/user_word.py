from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.models.base import Base
from app.db.models.file_word import FileWord


# Сущность, в которой хранятся слова (уникальные) после обработки импорта
class UserWord(Base):
    __tablename__ = "user_word"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, nullable=False)
    word: Mapped[str] = mapped_column(String(50), nullable=False)

    file: Mapped["FileWord"] = (
        relationship("FileWord", back_populates="user_word", cascade="all, delete-orphan"))

    def __repr__(self):
        return f"Word(id={self.id!r}, word={self.word!r})"
