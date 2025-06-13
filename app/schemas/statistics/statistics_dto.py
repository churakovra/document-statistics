from uuid import UUID

from pydantic import BaseModel


class StatisticsDTO(BaseModel):
    uuid: UUID
    stat_type: int
    source_uuid: UUID
    word: str
    tf: float
    idf: float