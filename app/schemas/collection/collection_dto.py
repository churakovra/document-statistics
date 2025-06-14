from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class CollectionDTO(BaseModel):
    uuid: UUID
    label: str
    user_create: UUID
    dt_create: datetime
    base: bool
