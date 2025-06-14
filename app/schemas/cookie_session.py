from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class CookieSession(BaseModel):
    user_session: UUID
    dt_exp: datetime