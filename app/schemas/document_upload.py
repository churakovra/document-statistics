from pydantic import BaseModel

from app.schemas.collection_dto import CollectionDTO
from app.schemas.document_response import DocumentResponse


class DocumentUploadResponse(BaseModel):
    collection: CollectionDTO
    document: DocumentResponse
