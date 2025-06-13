from http import HTTPStatus
from uuid import UUID

from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from sqlalchemy.orm import Session

from app.db.database import get_session
from app.enums.app_enums import HandlerTypes
from app.exceptions.user_exceptions import UserWrongPasswordException, UserNotFoundException
from app.schemas.user.user_account_response import UserAccountResponse
from app.schemas.user.user_change_password import UserChangePassword
from app.services.user_service import UserService

router = APIRouter()


@router.patch(
    path="/user/{user_id}",
    tags=[HandlerTypes.USER],
    response_model=UserAccountResponse,
    status_code=HTTPStatus.OK,
    summary="Изменение пароля",
    description="Проверка существования пользователя; проверка старого пароля; установка нового пароля",
    responses={
        HTTPStatus.OK: {"description": "Пароль успешно изменен"},
        HTTPStatus.NOT_FOUND: {"description": "Пользователь не найден"},
        HTTPStatus.BAD_REQUEST: {"description": "Некорректный старый пароль"},
    }
)
async def change_password(
        user_id: UUID,
        ucp: UserChangePassword,
        session: Session = Depends(get_session)
):
    try:
        user_service = UserService(session)
        user_service.change_password(user_id, ucp)
        return UserAccountResponse(message="Пароль успешно изменен", status_code=HTTPStatus.OK)
    except UserNotFoundException as nf:
        raise HTTPException(status_code=nf.status_code, detail=nf.message)
    except UserWrongPasswordException as wp:
        raise HTTPException(status_code=wp.status_code, detail=wp.message)
