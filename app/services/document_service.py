import os
import string
from datetime import datetime
from uuid import UUID

from fastapi import UploadFile
from sqlalchemy.orm import Session

from app.enums.app_enums import StatisticsTypes
from app.exceptions.document_exceptions import DocumentNotFoundException, DocumentsNotFoundException, \
    DocumentCollectionsNotFoundException
from app.repositories.document_repository import DocumentRepository
from app.repositories.statistics_repository import StatisticsRepository
from app.schemas.document.document_dto import DocumentDTO
from app.schemas.document.document_response import DocumentResponse
from app.schemas.user.user_dto import UserDTO
from app.services.statistics_service import StatisticsService


class DocumentService:
    def __init__(self, session: Session):
        self.db = session

    def _get_user_documents(self, user: UserDTO) -> dict[UUID, DocumentDTO]:
        document_repository = DocumentRepository(self.db)
        documents = document_repository.get_user_documents(user)
        if len(documents) <= 0:
            raise DocumentsNotFoundException(user.username)
        return documents

    def get_user_documents(self, user: UserDTO) -> dict[UUID, DocumentResponse]:
        documents = self._get_user_documents(user)
        documents_response = dict[UUID, DocumentResponse]()
        for uuid, document in documents.items():
            documents_response[uuid] = DocumentResponse(
                uuid=document.uuid,
                user_load=user.username,
                label=document.path.split("/").pop(),
                dt_load=document.dt_load
            )
        return documents_response

    def _get_document(self, document_uuid: UUID) -> DocumentDTO:
        document_repository = DocumentRepository(self.db)
        document = document_repository.get_document(document_uuid)
        if document is None:
            raise DocumentNotFoundException(document_uuid)
        return document

    def get_document(self, document_uuid: UUID, username: str) -> DocumentResponse:
        document = self._get_document(document_uuid)
        return DocumentResponse(
            uuid=document.uuid,
            user_load=username,
            label=document.path.split("/").pop(),
            dt_load=document.dt_load
        )

    def get_documents(self, documents_uuid: list[UUID], username: str) -> list[DocumentResponse]:
        return [self.get_document(document_uuid, username) for document_uuid in documents_uuid]

    async def upload_document(self, document: UploadFile, user: UserDTO) -> UUID:
        file_path = await self.write_document(document, user.username)
        document_repository = DocumentRepository(self.db)
        return document_repository.add_document(file_path, user)

    async def write_document(self, document: UploadFile, username: str) -> str:
        content_bytes = await document.read()
        if not content_bytes:
            raise ValueError("Файл пустой")
        upload_dir = "/app/storage/"
        os.makedirs(upload_dir, exist_ok=True)
        file_path = os.path.join(upload_dir, f"{username}_{datetime.now().timestamp()}_{document.filename}")
        with open(file_path, "wb") as out_file:
            out_file.write(content_bytes)
        return file_path

    def read_document(self, document_uuid: UUID) -> str:
        document = self._get_document(document_uuid)
        with open(file=document.path) as doc:
            content = doc.read()
        return content

    def read_documents(self, documents_uuid: list[UUID]) -> dict[UUID, list[str]]:
        documents = dict[UUID, list[str]]()
        for uuid in documents_uuid:
            document = self._get_document(uuid)
            document_words = [word.strip(string.punctuation).lower() for word in self.read_document(uuid).split()]
            documents[document.uuid] = document_words
        return documents

    def delete_document(self, document_uuid: UUID):
        document = self._get_document(document_uuid)

        try:
            os.remove(document.path)
        except FileNotFoundError:
            pass

        document_repository = DocumentRepository(self.db)
        document_repository.delete_document(document.uuid)

    def get_document_collections(self, document_uuid: UUID) -> list[UUID]:
        document_repository = DocumentRepository(self.db)
        collections_uuid = document_repository.get_document_collections(document_uuid)
        if len(collections_uuid) <= 0:
            raise DocumentCollectionsNotFoundException(document_uuid)
        return collections_uuid

    def get_statistics(self, document_uuid: UUID, documents_uuid: list[UUID]) -> dict[str, dict[str, float]]:
        statistics = StatisticsService()
        documents = self.read_documents(documents_uuid)
        tf = statistics.get_tf(documents[document_uuid])
        idf = statistics.get_idf(tf, documents)
        idf = statistics.sort_statistics(idf)

        statistics_repository = StatisticsRepository(self.db)
        for word, stat in idf.items():
            statistics_repository.add_statistics(
                stat_type=StatisticsTypes.DOCUMENT.value,
                source_uuid=document_uuid,
                word=word,
                tf=stat["tf"],
                idf=stat["idf"]
            )

        return idf
