from uuid import UUID

from sqlalchemy.orm import Session

from app.exceptions.collection_exceptions import BaseCollectionNotFoundException, CollectionEmptyException
from app.repositories.collectoin_repository import CollectionRepository
from app.schemas.collection.collection_dto import CollectionDTO
from app.schemas.user.user_dto import UserDTO


class CollectionService:
    def __init__(self, session: Session):
        self.db = session

    def get_base_collection(self, user_uuid: UUID) -> CollectionDTO:
        collection_repository = CollectionRepository(self.db)
        collection = collection_repository.get_base_collection(user_uuid)
        if collection is None:
            raise BaseCollectionNotFoundException()
        return collection

    def make_base_collection(self, user: UserDTO):
        collection_repository = CollectionRepository(self.db)
        new_collection_dto = collection_repository.create_collection(user_uuid=user.uuid, base=True)
        return new_collection_dto

    def add_document_to_base_collection(self, user: UserDTO, document_uuid: UUID) -> UUID:
        collection_repository = CollectionRepository(self.db)
        return collection_repository.add_document_to_base_collection(document_uuid, user.uuid)

    def add_document(self, collection: CollectionDTO, document_uuid: UUID) -> UUID:
        collection_repository = CollectionRepository(self.db)
        return collection_repository.add_document_to_collection(document_uuid, collection.uuid)

    def remove_document(self, document_uuid: UUID):
        collection_repository = CollectionRepository(self.db)
        collection_repository.remove_document(document_uuid)

    def get_collection_documents(self, collection_uuid: UUID) -> list[UUID]:
        collection_repository = CollectionRepository(self.db)
        documents_uuid = collection_repository.get_collection_documents(collection_uuid)
        if len(documents_uuid) <= 0:
            raise CollectionEmptyException(collection_uuid)
        return documents_uuid
