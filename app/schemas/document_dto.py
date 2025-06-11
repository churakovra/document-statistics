from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class DocumentDTO(BaseModel):
    uuid: UUID
    label: str
    user_load: str # username
    dt_load: datetime