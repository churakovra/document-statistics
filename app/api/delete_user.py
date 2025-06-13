from http import HTTPStatus
from uuid import UUID

from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from sqlalchemy.orm import Session

from app.db.database import get_session
from app.enums.app_enums import HandlerTypes
from app.exceptions.user_exceptions import UserNotFoundException
from app.services.user_service import UserService

router = APIRouter()


@router.delete(
    path="/user/{user_id}",
    tags=[HandlerTypes.USERS],
    status_code=HTTPStatus.NO_CONTENT,
    summary="Удаление пользователя",
    description="Удаление аккаунта. Пользователь должен быть авторизован. Удалить можно только свой аккаунт",
    responses={
        HTTPStatus.NO_CONTENT: {"description": "Пользователь успешно удален"}
    }
)
async def delete_user(
        user_id: UUID,
        session: Session = Depends(get_session)
):
    try:
        user_service = UserService(session)
        user_service.delete_user(user_id)
    except UserNotFoundException as nf:
        raise HTTPException(status_code=nf.status_code, detail=nf.message)
