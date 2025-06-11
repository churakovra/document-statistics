from http import HTTPStatus


class DocumentsIsNotFound(Exception):
    def __init__(self, username: str):
        self.message = f"Documents uploaded by {username} were not found."
        self.status_code = HTTPStatus.NOT_FOUND