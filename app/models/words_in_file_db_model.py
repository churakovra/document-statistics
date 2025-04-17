from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base_db_model import Base

if TYPE_CHECKING:
    from user_words_db_model import UserWords
    from user_files_db_model import UserFiles


# Сущность, в которой хранятся все слова из всех файлов после обработки импорта
class FileWords(Base):
    __tablename__ = "file_words"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, nullable=False)
    id_file: Mapped[int] = mapped_column(ForeignKey("user_files.id"), nullable=False)
    id_word: Mapped[int] = mapped_column(ForeignKey("user_words.id"), nullable=False)

    user_files: Mapped["UserFiles"] = relationship("UserFiles", back_populates="words")
    user_words: Mapped["UserWords"] = relationship("UserWords", back_populates="files")

    def __repr__(self) -> str:
        return f"FileWord(id={self.id!r}, id_file={self.id_file}, id_word={self.id_word})"
