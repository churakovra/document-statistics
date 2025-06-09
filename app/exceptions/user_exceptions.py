from http import HTTPStatus


class UserNotFoundException(Exception):
    def __init__(self, username: str):
        self.message = f"User {username} is not found"
        self.status_code = HTTPStatus.NOT_FOUND

class UserWrongPasswordException(Exception):
    def __init__(self):
        self.message = f"Password is wrong"
        self.status_code = HTTPStatus.BAD_REQUEST