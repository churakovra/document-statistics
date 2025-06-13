from pydantic import BaseModel


class UserChangePassword(BaseModel):
    username: str
    password_old: str
    password_new: str