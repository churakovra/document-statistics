from http import HTTPStatus
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_session
from app.dependencies.auth import get_current_user
from app.dependencies.collection_validate import validate_collection
from app.dependencies.document_validate import validate_document
from app.enums.app_enums import HandlerTypes
from app.exceptions.collection_exceptions import BaseCollectionNotFoundException, BaseCollectionDocumentRemoveException
from app.schemas.user.user_dto import UserDTO
from app.services.collection_service import CollectionService

router = APIRouter()


@router.delete(
    path="/collections/{collection_id}/{document_id}",
    tags=[HandlerTypes.COLLECTIONS],
    status_code=HTTPStatus.NO_CONTENT,
    summary="Удалить документ из коллекции",
    description="Документ удаляется из коллекции, не с диска. "
                "При удалении из кастомной коллекции документ присваивается базовой коллекции. "
                "Удаление документа из базовой коллекции невозможно",
    responses={
        HTTPStatus.NO_CONTENT: {"description": "Операция успешно выполнена"},
        HTTPStatus.NOT_FOUND: {"description": "Ресурс Коллекция/Документ не найден"},
        HTTPStatus.CONFLICT: {"description": "Невозможно удалить документ из базовой коллекции"}
    }
)
async def delete_document_collection(
        collection_id: UUID = Depends(validate_collection),
        document_id: UUID = Depends(validate_document),
        user: UserDTO = Depends(get_current_user),
        session: Session = Depends(get_session)
):
    try:
        collection_service = CollectionService(session)
        collection_service.remove_document(collection_uuid=collection_id, document_uuid=document_id, user=user)
    except BaseCollectionNotFoundException as bnf:
        raise HTTPException(status_code=bnf.status_code, detail=bnf.message)
    except BaseCollectionDocumentRemoveException as bcr:
        raise HTTPException(status_code=bcr.status_code, detail=bcr.message)
