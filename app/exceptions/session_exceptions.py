from http import HTTPStatus
from uuid import UUID


class SessionIsNoneException(Exception):
    def __init__(self):
        self.message = "Unauthorized, session is None"
        self.status_code = HTTPStatus.UNAUTHORIZED


class SessionNotFoundException(Exception):
    def __init__(self, session_uuid: UUID | str):
        self.message = f"Session {session_uuid} not found"
        self.status_code = HTTPStatus.NOT_FOUND


class SessionIsOldException(Exception):
    def __init__(self, session_uuid: UUID | str):
        self.message = f"Session {session_uuid} is old"
        self.status_code = HTTPStatus.INTERNAL_SERVER_ERROR
