import os
import string
from datetime import datetime
from uuid import UUID

from fastapi import UploadFile
from sqlalchemy.orm import Session

from app.config.preferences import AVAILABLE_LETTERS_LOWER
from app.enums.app_enums import StatisticsTypes
from app.exceptions.document_exceptions import DocumentNotFoundException, DocumentsNotFoundException, \
    DocumentCollectionsNotFoundException, DocumentIsEmptyException, DocumentWrongTypeException
from app.repositories.document_repository import DocumentRepository
from app.repositories.statistics_repository import StatisticsRepository
from app.schemas.document.document_dto import DocumentDTO
from app.schemas.document.document_response import DocumentResponse
from app.schemas.user.user_dto import UserDTO
from app.services.security_service import SecurityService
from app.services.statistics_service import StatisticsService
from app.utils.binary_node import BinaryNode
from app.utils.priority_heap import PriorityHeap


class DocumentService:
    def __init__(self, session: Session):
        self.db = session

    def _get_user_documents(self, user: UserDTO) -> dict[UUID, DocumentDTO]:
        document_repository = DocumentRepository(self.db)
        documents = document_repository.get_user_documents(user.uuid)
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

    def validate_document(self, file_name: str):
        file_type = file_name.split(".")[1]
        if not file_name.split(".")[1] == "txt":
            raise DocumentWrongTypeException(file_type)

    async def write_document(self, document: UploadFile, username: str) -> str:
        content_bytes = await document.read()
        if not content_bytes:
            raise DocumentIsEmptyException(None)
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

    def read_document_letters(self, document_uuid) -> tuple[list, dict[str, float | None]]:
        document_content = []
        document_letters = dict[str, float | None]()

        for letter in self.read_document(document_uuid):
            letter_lower = letter.lower()
            if letter_lower in AVAILABLE_LETTERS_LOWER:
                document_content.append(letter_lower)
                if letter_lower not in document_letters.keys():
                    document_letters[letter_lower] = None

        return document_content, document_letters

    def delete_document(self, document_uuid: UUID):
        document = self._get_document(document_uuid)
        try:
            os.remove(document.path)
        except FileNotFoundError:
            pass
        document_repository = DocumentRepository(self.db)
        document_repository.delete_document(document.uuid)

    def delete_user_documents(self, user: UserDTO) -> list[UUID]:
        deleted_uuids = []
        try:
            documents = self._get_user_documents(user)
            for uuid in documents:
                self.delete_document(uuid)
                deleted_uuids.append(uuid)
        except DocumentsNotFoundException:
            pass
        return deleted_uuids

    def get_document_collections(self, document_uuid: UUID) -> list[UUID]:
        document_repository = DocumentRepository(self.db)
        collections_uuid = document_repository.get_document_collections(document_uuid)
        if len(collections_uuid) <= 0:
            raise DocumentCollectionsNotFoundException(document_uuid)
        return collections_uuid

    def get_statistics(self, document_uuid: UUID, documents_uuid: list[UUID]) -> dict[str, dict[str, float]]:
        statistics_service = StatisticsService()
        statistics_repository = StatisticsRepository(self.db)
        statistics = statistics_repository.get_statistics(document_uuid)
        if len(statistics) > 0:
            response = statistics_service.get_statistics_response(statistics)
            return response

        documents = self.read_documents(documents_uuid)
        try:
            statistics = statistics_service.get_statistics(documents[document_uuid], documents)
        except ValueError:
            raise DocumentIsEmptyException(document_uuid)
        statistics = statistics_service.sort_statistics(statistics)

        for word, stat in statistics.items():
            statistics_repository.add_statistics(
                stat_type=StatisticsTypes.COLLECTION.value,  # Статистика документа в коллекции
                source_uuid=document_uuid,
                word=word,
                tf=stat["tf"],
                idf=stat["idf"]
            )

        return statistics

    def read_document_huffman(self, document_uuid: UUID) -> str:

        document_content, document_letters = self.read_document_letters(document_uuid)

        for search_letter in document_letters:
            letter_cnt = 0
            for letter in document_content:
                if letter == search_letter:
                    letter_cnt += 1
            document_letters[search_letter] = letter_cnt / len(document_content)

        priority_heap = PriorityHeap()
        priority_heap.fill(document_letters)

        while len(priority_heap.data) > 1:
            left_node, left_priority = priority_heap.pop()
            right_node, right_priority = priority_heap.pop()
            node = BinaryNode(value=None, left=left_node, right=right_node)
            priority_heap.add(item=node, priority=left_priority + right_priority)

        root = priority_heap.pop()[0]
        codes = SecurityService.generate_code(root)

        response = ""

        for letter in document_content:
            letter_lower = letter.lower()
            response += codes[letter_lower]

        return response
