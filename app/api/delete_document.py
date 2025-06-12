from http import HTTPStatus
from uuid import UUID

from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from sqlalchemy.orm import Session

from app.db.database import get_session
from app.dependencies.auth import get_current_user
from app.enums.app_enums import HandlerTypes
from app.exceptions.document_exceptions import DocumentNotFoundException
from app.schemas.user_dto import UserDTO
from app.services.collection_service import CollectionService
from app.services.document_service import DocumentService

router = APIRouter()

@router.delete(
    path="/documents/{document_id}",
    tags=[HandlerTypes.DOCUMENT],
    status_code=HTTPStatus.NO_CONTENT
)
async def delete_document(
        document_id: UUID,
        user: UserDTO = Depends(get_current_user),
        session: Session = Depends(get_session)
):
    document_service = DocumentService(session)
    collection_service = CollectionService(session)
    try:
        collection_service.remove_document(document_id)
        document_service.delete_document(document_id)
    except DocumentNotFoundException as nf:
        raise HTTPException(status_code=nf.status_code, detail=nf.message)