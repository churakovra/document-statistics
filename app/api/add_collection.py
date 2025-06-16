from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_session
from app.dependencies.auth import get_current_user
from app.enums.app_enums import HandlerTypes
from app.exceptions.collection_exceptions import CollectionLabelException
from app.schemas.collection.collection_dto import CollectionDTO
from app.schemas.collection.new_collection import NewCollection
from app.schemas.user.user_dto import UserDTO
from app.services.collection_service import CollectionService

router = APIRouter()


@router.post(
    path="/collections",
    tags=[HandlerTypes.COLLECTIONS],
    response_model=CollectionDTO,
    status_code=HTTPStatus.OK,
    summary="Создать коллекцию",
    description="Создание новой коллекции. Необходимо в теле запроса передать имя новой коллекции "
                "Если у пользователя ещё нет коллекций - создается базовая, иначе создается коллекция без флага base",
    responses={
        HTTPStatus.OK: {"description": "Операция успешно выполнена"},
    }
)
async def add_collection(
        label: NewCollection,
        user: UserDTO = Depends(get_current_user),
        session: Session = Depends(get_session)
):
    try:
        collection_service = CollectionService(session)
        return collection_service.make_collection(user, label=label.label)
    except CollectionLabelException as cle:
        raise HTTPException(status_code=cle.status_code, detail=cle.message)
