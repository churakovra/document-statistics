from datetime import datetime

from pydantic import BaseModel


class UserFile(BaseModel):
    file_name: str
    load_datetime: datetime
    user: str
    words: list[str]
