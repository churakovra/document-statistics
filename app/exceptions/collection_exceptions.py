from http import HTTPStatus
from uuid import UUID


class BaseCollectionNotFoundException(Exception):
    def __init__(self):
        self.message = f"Base collection  were not found"
        self.status_code = HTTPStatus.NOT_FOUND

class CollectionEmptyException(Exception):
    def __init__(self, collection_uuid: UUID):
        self.message = f"Collection {collection_uuid} does not have any documents"
        self.status_code = HTTPStatus.NOT_FOUND
