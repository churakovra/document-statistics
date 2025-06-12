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
from app.services.document_service import DocumentService

router = APIRouter()


@router.get(
    path="/documents/{document_id}",
    tags=[HandlerTypes.DOCUMENT],
    response_model=str,
    status_code=HTTPStatus.OK,
    summary="Получить содержание документа",
    description="Содержание документа в формате строки",
    responses={
        HTTPStatus.OK: {"description": "Операция успешно выполнена"},
        HTTPStatus.NOT_FOUND: {"description": "Документ с <document_id> не найден"}
    }
)
async def get_document_content(
        document_id: UUID,
        user: UserDTO = Depends(get_current_user),
        session: Session = Depends(get_session)
):
    document_service = DocumentService(session)
    try:
        print("Хочу прочитать документ")
        content = document_service.read_document(document_id)
    except DocumentNotFoundException as nf:
        raise HTTPException(status_code=nf.status_code, detail=nf.message)
    return content
