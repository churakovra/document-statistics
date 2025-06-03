from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.models.base import Base

if TYPE_CHECKING:
    from user_word import UserWord
    from user_file import UserFile


# Сущность, в которой хранятся все слова из всех файлов после обработки импорта
class FileWord(Base):
    __tablename__ = "file_word"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, nullable=False)
    id_file: Mapped[int] = mapped_column(ForeignKey("user_file.id"), nullable=False)
    id_word: Mapped[int] = mapped_column(ForeignKey("user_word.id"), nullable=False)

    user_file: Mapped["UserFile"] = relationship("UserFile", back_populates="word")
    user_word: Mapped["UserWord"] = relationship("UserWord", back_populates="file")

    def __repr__(self) -> str:
        return f"FileWord(id={self.id!r}, id_file={self.id_file}, id_word={self.id_word})"
