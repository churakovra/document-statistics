from datetime import datetime

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List

from app.models.base_db_model import Base
from app.models.file_contents_db_model import FileContents


class UserFile(Base):
    __tablename__ = "user_file"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, nullable=False)
    file_name: Mapped[str] = mapped_column(String(50), nullable=False)
    load_datetime: Mapped[datetime] = mapped_column(default=datetime.now, nullable=False)
    user: Mapped[str] = mapped_column(String(16), nullable=False)
    words: Mapped[List["FileContents"]] = relationship(back_populates="file")

    def __repr__(self) -> str:
        return (f"File("
                f"id={self.id!r}, "
                f"file_name={self.file_name!r}, "
                f"load_datetime={self.load_datetime!r}, "
                f"user={self.user!r})")
