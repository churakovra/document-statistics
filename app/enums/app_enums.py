from enum import Enum


class Status(str, Enum):
    OK = "OK"
    ERROR = "ERROR"


class SessionCookieKey(str, Enum):
    SESSION = "user_session"
    DT_EXP = "dt_exp"


class HandlerTypes(str, Enum):
    USER = "user"
    DOCUMENT = "document"
