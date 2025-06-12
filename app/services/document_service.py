import os
from datetime import datetime
from uuid import UUID

from fastapi import UploadFile
from sqlalchemy.orm import Session

from app.exceptions.document_exceptions import DocumentNotFoundException, DocumentsNotFoundException
from app.repositories.document_repository import DocumentRepository
from app.schemas.document_dto import DocumentDTO
from app.schemas.document_response import DocumentResponse
from app.schemas.user_dto import UserDTO


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
        for uuid, document in documents:
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
