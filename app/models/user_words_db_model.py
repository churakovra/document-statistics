from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base_db_model import Base
from app.models.words_in_file_db_model import FileWords


# Сущность, в которой хранятся слова (уникальные) после обработки импорта
class UserWords(Base):
    __tablename__ = "user_words"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, nullable=False)
    word: Mapped[str] = mapped_column(String(50), nullable=False)

    files: Mapped["FileWords"] = (
        relationship("FileWords", back_populates="user_words", cascade="all, delete-orphan"))

    def __repr__(self):
        return f"Word(id={self.id!r}, word={self.word!r})"
