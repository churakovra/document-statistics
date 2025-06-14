from http import HTTPStatus
from uuid import UUID

from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from sqlalchemy.orm import Session

from app.db.database import get_session
from app.dependencies.auth import get_current_user
from app.enums.app_enums import HandlerTypes
from app.exceptions.collection_exceptions import BaseCollectionNotFoundException, CollectionsNotFoundException
from app.exceptions.document_exceptions import DocumentNotFoundException
from app.schemas.user.user_dto import UserDTO
from app.services.collection_service import CollectionService
from app.services.document_service import DocumentService

router = APIRouter()


@router.delete(
    path="/documents/{document_id}",
    tags=[HandlerTypes.DOCUMENTS],
    status_code=HTTPStatus.NO_CONTENT,
    summary="Удаление документа",
    description="Удаление документа с диска и из всех коллекций",
    responses={
        HTTPStatus.NO_CONTENT: {"description": "Операция выполнена успешно"},
        HTTPStatus.NOT_FOUND: {"description": "Документ с <document_id> не найден"},
    }
)
async def delete_document(
        document_id: UUID,
        user: UserDTO = Depends(get_current_user),
        session: Session = Depends(get_session)
):
    document_service = DocumentService(session)
    collection_service = CollectionService(session)
    try:
        collection_service.remove_document_from_all_collections(document_uuid=document_id)
        document_service.delete_document(document_id)
        return {"message": "Операция успешно выполнена"}
    except DocumentNotFoundException as dnf:
        raise HTTPException(status_code=dnf.status_code, detail=dnf.message)
    except BaseCollectionNotFoundException as bnf:
        raise HTTPException(status_code=bnf.status_code, detail=bnf.message)
    except CollectionsNotFoundException as cnf:
        raise HTTPException(status_code=cnf.status_code, detail=cnf.message)
