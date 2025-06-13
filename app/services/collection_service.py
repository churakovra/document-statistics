from uuid import UUID

from sqlalchemy.orm import Session

from app.enums.app_enums import StatisticsTypes
from app.exceptions.collection_exceptions import BaseCollectionNotFoundException, CollectionEmptyException, \
    CollectionsNotFoundException, CollectionNotFoundException
from app.repositories.collectoin_repository import CollectionRepository
from app.repositories.statistics_repository import StatisticsRepository
from app.schemas.collection.collection_dto import CollectionDTO
from app.schemas.collection.collection_response import CollectionResponse
from app.schemas.user.user_dto import UserDTO
from app.services.document_service import DocumentService
from app.services.statistics_service import StatisticsService


class CollectionService:
    def __init__(self, session: Session):
        self.db = session

    def get_base_collection(self, user_uuid: UUID) -> CollectionDTO:
        collection_repository = CollectionRepository(self.db)
        collection = collection_repository.get_base_collection(user_uuid)
        if collection is None:
            raise BaseCollectionNotFoundException(user_uuid)
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

    def _get_collections(self, user_uuid: UUID) -> list[CollectionDTO]:
        collection_repository = CollectionRepository(self.db)
        collections = collection_repository.get_collections(user_uuid)
        if len(collections) <= 0:
            raise CollectionsNotFoundException(user_uuid)
        return collections

    def _get_collection(self, collection_uuid: UUID):
        collection_repository = CollectionRepository(self.db)
        collection = collection_repository.get_collection(collection_uuid)
        if collection is None:
            raise CollectionNotFoundException(collection_uuid)
        return collection

    def get_collections_with_documents(self, user: UserDTO) -> list[CollectionResponse]:
        collections = self._get_collections(user.uuid)
        documents_uuid = [self.get_collection_documents(collection.uuid) for collection in collections]
        document_service = DocumentService(self.db)
        response = list()
        for index, collection in enumerate(documents_uuid):
            documents = document_service.get_documents(collection, user.username)
            response.append(
                CollectionResponse(
                    collection_uuid=collections[index].uuid,
                    documents=documents
                )
            )
        return response

    def get_statistics(self, collection_uuid: UUID) -> dict[str, dict[str, float]]:
        statistics_service = StatisticsService()
        statistics_repository = StatisticsRepository(self.db)
        statistics = statistics_repository.get_statistics(collection_uuid)
        if len(statistics) > 0:
            response = statistics_service.get_statistics_response(statistics)
            return response

        documents_uuid = self.get_collection_documents(collection_uuid)
        document_service = DocumentService(self.db)
        documents = document_service.read_documents(documents_uuid)
        collection = list[str]()
        for words in documents.values():
            collection.extend(words)
        tf = statistics_service.get_tf(collection)
        idf = statistics_service.get_idf(tf, documents)
        idf = statistics_service.sort_statistics(idf)

        for word, stat in idf.items():
            statistics_repository.add_statistics(
                stat_type=StatisticsTypes.COLLECTION.value,  # Статистика коллекции
                source_uuid=collection_uuid,
                word=word,
                tf=stat["tf"],
                idf=stat["idf"]
            )

        return idf
