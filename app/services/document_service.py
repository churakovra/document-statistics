from uuid import UUID

from sqlalchemy.orm import Session

from app.exceptions.document_exceptions import DocumentsIsNotFound
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
            raise DocumentsIsNotFound(user.username)
        return documents
