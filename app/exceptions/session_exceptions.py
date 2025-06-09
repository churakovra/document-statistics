from http import HTTPStatus


class SessionIsNoneException(Exception):
    def __init__(
            self,
            message: str = "Check session error, session is None. Redirect to /login"
    ):
        self.message = message
        self.status_code = HTTPStatus.TEMPORARY_REDIRECT