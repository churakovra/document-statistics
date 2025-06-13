import uuid
from datetime import datetime
from uuid import UUID

from sqlalchemy import select, delete
from sqlalchemy.orm import Session

from app.db.models.user_account import UserAccount
from app.db.models.user_session import UserSession

from app.db.models.document import Document
from app.db.models.collection import Collection
from app.db.models.collection_documents import CollectionDocuments

from app.db.models.statistics import Statistics
from app.schemas.document.document_dto import DocumentDTO
from app.schemas.user.user_dto import UserDTO


class DocumentRepository:
    def __init__(self, session: Session):
        self.db = session

    def get_user_documents(self, user: UserDTO) -> dict[UUID, DocumentDTO]:
        stmt = select(Document).where(Document.user_load == user.uuid)
        documents = dict[UUID, DocumentDTO]()
        for document in self.db.scalars(stmt):
            document_dto = DocumentDTO(
                uuid=document.uuid,
                path=document.path,
                user_load=user.uuid,
                dt_load=document.dt_load
            )
            documents[document_dto.uuid] = document_dto
        return documents

    def get_document(self, document_uuid: UUID) -> DocumentDTO | None:
        stmt = select(Document).where(Document.uuid == document_uuid)
        document = self.db.scalar(stmt)
        if document is None:
            return document
        document_dto = DocumentDTO(
            uuid=document.uuid,
            path=document.path,
            user_load=document.user_load,
            dt_load=document.dt_load
        )
        return document_dto

    def add_document(self, path: str, user: UserDTO) -> UUID:
        document = Document(
            uuid=uuid.uuid4(),
            path=path,
            user_load=user.uuid,
            dt_load=datetime.now()
        )
        self.db.add(document)
        self.db.commit()
        self.db.refresh(document)
        return document.uuid

    def delete_document(self, document_uuid: UUID):
        stmt = delete(Document).where(Document.uuid == document_uuid)
        self.db.execute(stmt)
        self.db.commit()

    def get_document_collections(self, document_uuid: UUID) -> list[UUID]:
        stmt = select(CollectionDocuments.uuid_collection).where(CollectionDocuments.uuid_document==document_uuid)
        collections = list[UUID]()
        for document_uuid in self.db.scalars(stmt):
            collections.append(document_uuid)
        return collections