import uuid
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

    @staticmethod
    def get_statistics_orm(stat_type: int, source_uuid: UUID, word: str, tf: float, idf: float):
        return Statistics(
            uuid=uuid.uuid4(),
            stat_type=stat_type,
            source_uuid=source_uuid,
            word=word,
            tf=tf,
            idf=idf
        )
