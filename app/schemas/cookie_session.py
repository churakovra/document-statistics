from uuid import UUID

from pydantic import BaseModel


class CookieSession(BaseModel):
    session_uuid: UUID
