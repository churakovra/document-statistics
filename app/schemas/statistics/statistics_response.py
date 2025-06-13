from pydantic import BaseModel


class StatisticsResponse(BaseModel):
    statistics: dict[str, dict[str, float]]
