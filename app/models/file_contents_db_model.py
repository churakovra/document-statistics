from typing import TYPE_CHECKING

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base_db_model import Base

if TYPE_CHECKING:
    from .user_file_db_model import UserFile


class FileContents(Base):
    __tablename__ = "file_contents"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, nullable=False)
    word: Mapped[str] = mapped_column(String(50), nullable=False)
    file_id: Mapped[int] = mapped_column(ForeignKey("user_file.id"), nullable=False)
    file: Mapped["UserFile"] = relationship("UserFile", back_populates="words")

    def __repr__(self):
        return f"Word(id={self.id!r}, word={self.word!r}, file={self.file!r})"
