from pydantic import BaseModel

from app.schemas.collection_dto import CollectionDTO
from app.schemas.document_dto import DocumentDTO


class DocumentUploadResponse(BaseModel):
    collection: CollectionDTO
    document: DocumentDTO
