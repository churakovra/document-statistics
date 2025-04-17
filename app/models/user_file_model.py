from datetime import datetime

from pydantic import BaseModel


class UserFile(BaseModel):
    file_name: str
    file_size: int
    load_datetime: datetime
    user: str
    words: list[str]
