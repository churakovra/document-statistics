from http import HTTPStatus
from uuid import UUID


class BaseCollectionNotFoundException(Exception):
    def __init__(self, user_uuid: UUID):
        self.message = f"Base collection for user {user_uuid} were not found"
        self.status_code = HTTPStatus.NOT_FOUND


class CollectionEmptyException(Exception):
    def __init__(self, collection_uuid: UUID):
        self.message = f"Collection {collection_uuid} does not have any documents"
        self.status_code = HTTPStatus.NOT_FOUND


class CollectionsNotFoundException(Exception):
    def __init__(self, user_uuid: UUID):
        self.message = f"User {user_uuid} collections  were not found"
        self.status_code = HTTPStatus.NOT_FOUND


class CollectionNotFoundException(Exception):
    def __init__(self, user_uuid: UUID):
        self.message = f"Collection {user_uuid} were not found"
        self.status_code = HTTPStatus.NOT_FOUND


class CollectionAlreadyHasDocumentException(Exception):
    def __init__(self, collection_uuid: UUID, document_uuid: UUID):
        self.message = f"Collection {collection_uuid} already has document {document_uuid}"
        self.status_code = HTTPStatus.CONFLICT

class BaseCollectionDocumentRemoveException(Exception):
    def __init__(self, collection_uuid: UUID, document_uuid: UUID):
        self.message = f"Can't delete form Base collection {collection_uuid} document {document_uuid}"
        self.status_code = HTTPStatus.CONFLICT
