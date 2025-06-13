from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class UserSessionDTO(BaseModel):
    uuid_session: UUID
    uuid_user: UUID
    dt_exp: datetime
    alive: bool
