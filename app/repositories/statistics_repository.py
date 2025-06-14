from uuid import UUID

from sqlalchemy import select, delete
from sqlalchemy.orm import Session

from app.db.models.statistics import Statistics
from app.schemas.statistics.statistics_dto import StatisticsDTO


class StatisticsRepository:
    def __init__(self, session: Session):
        self.db = session

    def get_statistics(self, source_uuid: UUID) -> list[StatisticsDTO]:
        stmt = select(Statistics).where(Statistics.source_uuid == source_uuid)
        statistics = list()
        for statistic in self.db.scalars(stmt):
            statistics.append(
                StatisticsDTO(
                    uuid=statistic.uuid,
                    stat_type=statistic.stat_type,
                    source_uuid=statistic.source_uuid,
                    word=statistic.word,
                    tf=statistic.tf,
                    idf=statistic.idf
                )
            )
        return statistics

    def add_statistics(self, stat_type: int, source_uuid: UUID, word: str, tf: float, idf: float):
        statistics = Statistics.get_statistics_orm(stat_type, source_uuid, word, tf, idf)
        self.db.add(statistics)
        self.db.commit()
        self.db.refresh(statistics)

    def delete_statistics(self, source_uuid: UUID):
        stmt = delete(Statistics).where(Statistics.source_uuid==source_uuid)
        self.db.execute(stmt)
        self.db.commit()

