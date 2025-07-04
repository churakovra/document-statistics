from http import HTTPStatus
from uuid import UUID

from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from sqlalchemy.orm import Session

from app.db.database import get_session
from app.dependencies.auth import get_current_user
from app.dependencies.document_validate import validate_document
from app.enums.app_enums import HandlerTypes
from app.exceptions.collection_exceptions import BaseCollectionNotFoundException, CollectionEmptyException
from app.schemas.statistics.statistics_response import StatisticsResponse
from app.schemas.user.user_dto import UserDTO
from app.services.collection_service import CollectionService
from app.services.document_service import DocumentService

router = APIRouter()


@router.get(
    path="/documents/{document_id}/statistics",
    tags=[HandlerTypes.DOCUMENTS],
    response_model=StatisticsResponse,
    status_code=HTTPStatus.OK,
    summary="Получение статистики документа",
    description="Получение статистики производится в контексте базовой коллекции",
    responses={
        HTTPStatus.OK: {"description": "Статистика получена"},
        HTTPStatus.NOT_FOUND: {
            "description": "Базовая коллекция не найдена / Коллекция пустая. Читать message возвращаемой ошибки"
        },
        HTTPStatus.CONFLICT: {
            "description": "Документ для расчета TF не может быть пустым"
        }
    }
)
async def get_document_statistics(
        document_id: UUID = Depends(validate_document),
        user: UserDTO = Depends(get_current_user),
        session: Session = Depends(get_session)
):
    try:
        collection_service = CollectionService(session)
        collection = collection_service.get_base_collection(user.uuid)

        document_service = DocumentService(session)
        documents = collection_service.get_collection_documents(collection.uuid)

        statistics = StatisticsResponse(statistics=document_service.get_statistics(document_id, documents))
        return statistics
    except BaseCollectionNotFoundException as bnf:
        raise HTTPException(status_code=bnf.status_code, detail=bnf.message)
    except CollectionEmptyException as ce:
        raise HTTPException(status_code=ce.status_code, detail=ce.message)
    except ValueError:
        raise HTTPException(status_code=HTTPStatus.CONFLICT, detail="The document should not be empty")
