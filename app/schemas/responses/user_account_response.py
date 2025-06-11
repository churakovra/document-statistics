from datetime import datetime
from http import HTTPStatus
from uuid import UUID

from pydantic import BaseModel


class UserCreds(BaseModel):
    uuid: UUID
    username: str
    dt_reg: datetime


class UserAccountResponse(BaseModel):
    message: str
    status_code: HTTPStatus
    user: UserCreds | None = None
