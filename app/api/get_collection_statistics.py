from http import HTTPStatus
from uuid import UUID

from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from sqlalchemy.orm import Session

from app.db.database import get_session
from app.dependencies.auth import get_current_user
from app.dependencies.collection_validate import validate_collection
from app.enums.app_enums import HandlerTypes
from app.exceptions.collection_exceptions import CollectionEmptyException
from app.exceptions.document_exceptions import DocumentNotFoundException
from app.schemas.statistics.statistics_response import StatisticsResponse
from app.schemas.user.user_dto import UserDTO
from app.services.collection_service import CollectionService

router = APIRouter()


@router.get(
    path="/collections/{collection_id}/statistics",
    tags=[HandlerTypes.COLLECTIONS],
    status_code=HTTPStatus.OK,
    response_model=StatisticsResponse,
    summary="Получить статистику коллекции",
    description="Получить статистику коллекции. Если данные о статистике есть в БД, возвращаются эти данные без пересчета",
    responses={
        HTTPStatus.OK: {"description": "Операция выполнена успешно"},
        HTTPStatus.NOT_FOUND: {"description": "Коллекция пустая / документ не найден. Читать в теле ошибки"},
        HTTPStatus.CONFLICT: {
            "description": "Документ для расчета TF не может быть пустым"
        }
    }
)
async def get_collection_statistics(
        collection_id: UUID = Depends(validate_collection),
        user: UserDTO = Depends(get_current_user),
        session: Session = Depends(get_session)
):
    try:
        collection_service = CollectionService(session)
        return StatisticsResponse(statistics=collection_service.get_statistics(collection_id))
    except CollectionEmptyException as ce:
        raise HTTPException(status_code=ce.status_code, detail=ce.message)
    except DocumentNotFoundException as dnf:
        raise HTTPException(status_code=dnf.status_code, detail=dnf.message)
    except ValueError:
        raise HTTPException(status_code=HTTPStatus.CONFLICT, detail="The collection documents should not be empty")
