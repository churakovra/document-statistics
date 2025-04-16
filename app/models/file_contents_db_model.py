from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base_db_model import Base
from app.models.user_file_db_model import UserFile

class FileContents(Base):
    __tablename__ = "file_contents"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, nullable=False)
    word: Mapped[str] = mapped_column(String(50), nullable=False)
    file: Mapped["UserFile"] = relationship(back_populates="words")

    def __repr__(self):
        return f"Word(id={self.id!r}, word={self.word!r}, file={self.file!r})"