from http import HTTPStatus
from uuid import UUID

from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from sqlalchemy.orm import Session

from app.db.database import get_session
from app.dependencies.auth import get_current_user
from app.enums.app_enums import HandlerTypes
from app.exceptions.document_exceptions import DocumentsIsNotFound
from app.schemas.document_dto import DocumentDTO
from app.schemas.user_dto import UserDTO
from app.services.document_service import DocumentService

router = APIRouter()


@router.get(
    path="/documents",
    tags=[HandlerTypes.DOCUMENT],
    response_model=dict[UUID, DocumentDTO],
    status_code=HTTPStatus.OK,
    summary="Получение списка файлов пользователя ",
    description="Получение всех файлов, загруженных текущим пользователем",
    responses={
        HTTPStatus.OK: {"description": "Файлы получены"},
        HTTPStatus.UNAUTHORIZED: {"description": "Сессия пользователя None. Необходима аутентификация"},
        HTTPStatus.NOT_FOUND: {"description": "Пользователь или Документ не найден"},
    }
)
async def get_documents(
        user: UserDTO = Depends(get_current_user),
        session: Session = Depends(get_session)
):
    document_service = DocumentService(session)
    try:
        documents = document_service.get_user_documents(user)
        return documents
    except DocumentsIsNotFound as nf:
        raise HTTPException(status_code=nf.status_code, detail=nf.message)
