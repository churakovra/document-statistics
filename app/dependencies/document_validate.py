from uuid import UUID

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_session
from app.exceptions.document_exceptions import DocumentNotFoundException
from app.services.document_service import DocumentService


def validate_document(
        document_id: UUID,
        session: Session = Depends(get_session)
):
    document_service = DocumentService(session)
    try:
        document = document_service._get_document(document_id)
        return document.uuid
    except DocumentNotFoundException as nf:
        raise HTTPException(status_code=nf.status_code, detail=nf.message)
