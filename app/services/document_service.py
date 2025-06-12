import os
from datetime import datetime
from uuid import UUID

from fastapi import UploadFile
from sqlalchemy.orm import Session

from app.exceptions.document_exceptions import DocumentNotFoundException, DocumentsNotFoundException
from app.repositories.document_repository import DocumentRepository
from app.schemas.document_dto import DocumentDTO
from app.schemas.user_dto import UserDTO


class DocumentService:
    def __init__(self, session: Session):
        self.db = session

    def get_user_documents(self, user: UserDTO) -> dict[UUID, DocumentDTO]:
        document_repository = DocumentRepository(self.db)
        documents = document_repository.get_user_documents(user)
        if len(documents) <= 0:
            raise DocumentsNotFoundException(user.username)
        return documents

    def get_document(self, document_uuid: UUID) -> DocumentDTO:
        document_repository = DocumentRepository(self.db)
        document = document_repository.get_document(document_uuid)
        if document is None:
            raise DocumentNotFoundException(document_uuid)
        return document

    async def upload_document(self, file: UploadFile, user: UserDTO) -> UUID:
        file_path = await self.write_document(file, user.username)
        document_repository = DocumentRepository(self.db)
        return document_repository.add_document(file_path, user)

    async def write_document(self, file, username: str) -> str:
        content_bytes = await file.read()
        if not content_bytes:
            raise ValueError("Файл пустой")
        upload_dir = "/app/storage/"
        os.makedirs(upload_dir, exist_ok=True)
        file_path = os.path.join(upload_dir, f"{username}_{datetime.now().timestamp()}_{file.filename}")
        with open(file_path, "wb") as out_file:
            out_file.write(content_bytes)
        return file_path
