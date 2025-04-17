from pydantic import BaseModel

from app.models.word_stat_response_model import WordStat

class FileStat(BaseModel):
    stat: list[WordStat]