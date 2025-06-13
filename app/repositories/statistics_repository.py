from uuid import UUID

from sqlalchemy.orm import Session

from app.db.models.statistics import Statistics


class StatisticsRepository:
    def __init__(self, session: Session):
        self.db = session

    def add_statistics(self, stat_type: int, source_uuid: UUID, word: str, tf: float, idf: float):
        statistics = Statistics.get_statistics_orm(stat_type, source_uuid, word, tf, idf)
        self.db.add(statistics)
        self.db.commit()
        self.db.refresh(statistics)
