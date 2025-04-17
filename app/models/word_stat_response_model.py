from pydantic import BaseModel

class WordStat(BaseModel):
    word: str
    tf: int
    dtf: int