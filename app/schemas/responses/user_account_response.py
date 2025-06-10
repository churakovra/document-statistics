from http import HTTPStatus

from pydantic import BaseModel

class UserAccountResponse(BaseModel):
    message: str
    status_code: HTTPStatus
