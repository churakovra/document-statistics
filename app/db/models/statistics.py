from uuid import UUID

from sqlalchemy.orm import Mapped, mapped_column

from app.db.models.base import Base


class Statistics(Base):
    __tablename__ = "statistics"

    uuid: Mapped[UUID] = mapped_column(primary_key=True)
    stat_type: Mapped[int]
    source_uuid: Mapped[UUID]
    word: Mapped[str]
    tf: Mapped[float]
    idf: Mapped[float]
