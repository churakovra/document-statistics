import uuid
from datetime import datetime
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models.user_account import UserAccount
from app.db.models.user_session import UserSession

from app.db.models.document import Document
from app.db.models.collection import Collection
from app.db.models.collection_documents import CollectionDocuments

from app.db.models.statistics import Statistics
from app.schemas.document_dto import DocumentDTO
from app.schemas.user_dto import UserDTO


class DocumentRepository:
    def __init__(self, session: Session):
        self.db = session

    def get_user_documents(self, user: UserDTO) -> dict[UUID, DocumentDTO]:
        stmt = select(Document).where(Document.user_load == user.uuid)
        documents = dict[UUID, DocumentDTO]()
        for document in self.db.scalars(stmt):
            document_dto = DocumentDTO(
                uuid=document.uuid,
                label=document.path.split("/").pop(),
                user_load=user.username,
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
            label=document.path.split("/").pop(),
            user_load=str(document.user_load),
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
