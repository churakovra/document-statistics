from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class DocumentResponse(BaseModel):
    uuid: UUID
    label: str
    user_load: str
    dt_load: datetime