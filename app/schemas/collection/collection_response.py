from uuid import UUID

from pydantic import BaseModel

from app.schemas.document.document_response import DocumentResponse


class CollectionResponse(BaseModel):
    uuid: UUID
    documents: list[DocumentResponse]