from datetime import datetime

from pydantic import BaseModel


class CookieSession(BaseModel):
    user_session: str
    dt_exp: datetime