from http import HTTPStatus
from uuid import UUID

from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.orm import Session

from app.db.database import get_session
from app.dependencies.auth import get_current_user
from app.dependencies.document_validate import validate_document
from app.enums.app_enums import HandlerTypes
from app.schemas.user.user_dto import UserDTO
from app.services.document_service import DocumentService

router = APIRouter()


@router.get(
    path="/documents/{document_id}/huffman",
    tags=[HandlerTypes.DOCUMENTS],
    status_code=HTTPStatus.OK,
    summary="Получение закодированного содержания документа",
    description="Получение содержания документа. Кодирование происходит по методу Хаффмана",
    responses={
        HTTPStatus.OK: {"description": "Операция выполнена успешно"},
        HTTPStatus.NOT_FOUND: {"description": "Документ не найден"},
    }
)
async def get_document_content_huffman(
        document_id: UUID = Depends(validate_document),
        user: UserDTO = Depends(get_current_user),
        session: Session = Depends(get_session)
):
    document_service = DocumentService(session)
    return document_service.read_document_huffman(document_id)
