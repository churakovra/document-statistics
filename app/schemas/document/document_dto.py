from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class DocumentDTO(BaseModel):
    uuid: UUID
    path: str
    user_load: UUID # username
    dt_load: datetime