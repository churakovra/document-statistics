from datetime import datetime

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.models.base import Base
from app.db.models.file_word import FileWord


# Сущность, в которой хранятся все файлы после обработки импорта
class UserFile(Base):
    __tablename__ = "user_file"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, nullable=False)
    file_name: Mapped[str] = mapped_column(String(50), nullable=False)
    file_size: Mapped[int] = mapped_column(nullable=False)
    load_datetime: Mapped[datetime] = mapped_column(default=datetime.now, nullable=False)
    user: Mapped[str] = mapped_column(String(16), nullable=False)

    word: Mapped["FileWord"] = (
        relationship("FileWord", back_populates="user_file", cascade="all, delete-orphan"))

    def __repr__(self) -> str:
        return (f"File("
                f"id={self.id!r},"
                f"file_name={self.file_name!r},"
                f"file_size={self.file_size!r},"
                f"load_datetime={self.load_datetime!r},"
                f"user={self.user!r})")
