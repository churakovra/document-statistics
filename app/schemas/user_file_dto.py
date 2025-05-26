from dataclasses import dataclass
from datetime import datetime

from pydantic import BaseModel

@dataclass
class UserFileDTO(BaseModel):
    file_name: str
    file_size: int
    load_datetime: datetime
    user: str
    words: list[str]
