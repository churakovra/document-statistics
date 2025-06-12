from uuid import UUID

from sqlalchemy.orm import Session

from app.exceptions.collection_exceptions import BaseCollectionNotFoundException
from app.repositories.collectoin_repository import CollectionRepository
from app.schemas.collection_dto import CollectionDTO
from app.schemas.user_dto import UserDTO


class CollectionService:
    def __init__(self, session: Session):
        self.db = session

    def check_base_collection(self, user: UserDTO) -> CollectionDTO:
        collection_repository = CollectionRepository(self.db)
        base_collection = collection_repository.get_base_collection(user_uuid=user.uuid)
        if base_collection is None:
            raise BaseCollectionNotFoundException()
        return base_collection

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
