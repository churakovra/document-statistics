from http import HTTPStatus

from pydantic import BaseModel

class LoginResponse(BaseModel):
    message: str
    status_code: HTTPStatus
