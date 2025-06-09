from http import HTTPStatus

from pydantic import BaseModel


class LoginFail(BaseModel):
    message: str
    status_code: HTTPStatus