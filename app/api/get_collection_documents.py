from http import HTTPStatus
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_session
from app.dependencies.auth import get_current_user
from app.dependencies.collection_validate import validate_collection
from app.enums.app_enums import HandlerTypes
from app.exceptions.collection_exceptions import CollectionEmptyException
from app.exceptions.document_exceptions import DocumentNotFoundException
from app.schemas.collection.collection_response import CollectionResponse
from app.schemas.user.user_dto import UserDTO
from app.services.collection_service import CollectionService
from app.services.document_service import DocumentService

router = APIRouter()


@router.get(
    path="/collections/{collection_id}",
    tags=[HandlerTypes.COLLECTIONS],
    response_model=CollectionResponse,
    status_code=HTTPStatus.OK,
    summary="Получить документы коллекции <collection_id>",
    description="Получение списка документов конкретной коллекции",
    responses={
        HTTPStatus.OK: {"description": "Операция выполнена успешно"},
        HTTPStatus.NOT_FOUND: {"description": "Коллекция не найдена / в коллекции нет документов"
                                              "Читать в теле ошибки"},
    }
)
async def get_collection_documents(
        collection_id: UUID = Depends(validate_collection),
        user: UserDTO = Depends(get_current_user),
        session: Session = Depends(get_session)
):
    try:
        collection_service = CollectionService(session)
        documents_uuid = collection_service.get_collection_documents(collection_id)
        document_service = DocumentService(session)
        documents = document_service.get_documents(documents_uuid, user.username)
        return CollectionResponse(collection_uuid=collection_id, documents=documents)
    except CollectionEmptyException as ce:
        raise HTTPException(status_code=ce.status_code, detail=ce.message)
    except DocumentNotFoundException as dnf:
        raise HTTPException(status_code=dnf.status_code, detail=dnf.message)
