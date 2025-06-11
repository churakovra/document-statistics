from http import HTTPStatus


class SessionIsNoneException(Exception):
    def __init__(
            self,
            message: str = "Unauthorized, session is None"
    ):
        self.message = message
        self.status_code = HTTPStatus.UNAUTHORIZED


class SessionNotFoundException(Exception):
    def __init__(self):
        self.message = "Session not found"
        self.status_code = HTTPStatus.NOT_FOUND
