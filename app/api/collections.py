from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_session
from app.dependencies.auth import get_current_user
from app.enums.app_enums import HandlerTypes
from app.exceptions.collection_exceptions import CollectionsNotFoundException, CollectionEmptyException
from app.schemas.collection.collection_response import CollectionResponse
from app.schemas.user.user_dto import UserDTO
from app.services.collection_service import CollectionService

router = APIRouter()


@router.get(
    path="/collections",
    response_model=list[CollectionResponse],
    tags=[HandlerTypes.COLLECTIONS],
    status_code=HTTPStatus.OK,
    summary="Получение всех коллекций и документов в коллекциях",
    description="Получение всех коллекций и документов в коллекциях авторизованного пользователя",
    responses={
        HTTPStatus.OK: {"description": "Операция выполнена успешно"},
        HTTPStatus.NOT_FOUND: {"description": "Коллекции не найдены / В коллекциях нет документов. "
                                              "Подробнее в теле ошибки"},
    }
)
async def get_collections(
        user: UserDTO = Depends(get_current_user),
        session: Session = Depends(get_session)
):
    collection_service = CollectionService(session)
    try:
        documents = collection_service.get_collections_with_documents(user)
        return documents
    except CollectionsNotFoundException as nf:
        raise HTTPException(status_code=nf.status_code, detail=nf.message)
    except CollectionEmptyException as ce:
        raise HTTPException(status_code=ce.status_code, detail=ce.message)
