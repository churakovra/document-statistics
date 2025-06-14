from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class UserDTO(BaseModel):
    uuid: UUID
    username: str
    password_hashed: str
    dt_reg: datetime
