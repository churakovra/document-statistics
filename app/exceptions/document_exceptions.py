from http import HTTPStatus
from uuid import UUID


class DocumentsNotFoundException(Exception):
    def __init__(self, username: str):
        self.message = f"Documents uploaded by {username} were not found."
        self.status_code = HTTPStatus.NOT_FOUND


class DocumentNotFoundException(Exception):
    def __init__(self, document_uuid: UUID):
        self.message = f"Document {document_uuid} were not found."
        self.status_code = HTTPStatus.NOT_FOUND


class DocumentCollectionsNotFoundException(Exception):
    def __init__(self, document_uuid: UUID):
        self.message = f"Document {document_uuid} collections were not found."


class DocumentIsEmptyException(Exception):
    def __init__(self, document_uuid: UUID | None):
        self.message = f"Document {document_uuid} is empty" if document_uuid \
            else "New document is empty, please try again"
        self.status_code = HTTPStatus.CONFLICT


class DocumentWrongTypeException(Exception):
    def __init__(self, document_type: str):
        self.message = f"Document `.{document_type}` can't be uploaded. Only `.txt` allowed"
        self.status_code = HTTPStatus.CONFLICT
