from pydantic import BaseModel


class NewUserAccount(BaseModel):
    username: str
    password: str