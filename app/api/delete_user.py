from http import HTTPStatus

from fastapi import APIRouter
from fastapi.params import Depends
from fastapi.responses import Response
from sqlalchemy.orm import Session

from app.db.database import get_session
from app.dependencies.auth import get_current_user
from app.enums.app_enums import HandlerTypes, SessionCookieKey as sck
from app.schemas.user.user_dto import UserDTO
from app.services.user_service import UserService

router = APIRouter()


@router.delete(
    path="/user",
    tags=[HandlerTypes.USERS],
    status_code=HTTPStatus.NO_CONTENT,
    summary="Удаление пользователя",
    description="Удаление аккаунта, информация о сессии которого находится в куках. "
                "Пользователь должен быть авторизован. Удалить можно только свой аккаунт",
    responses={
        HTTPStatus.NO_CONTENT: {"description": "Пользователь успешно удален"}
    }
)
async def delete_user(
        response: Response,
        user: UserDTO = Depends(get_current_user),
        session: Session = Depends(get_session),
):
    user_service = UserService(session)
    user_service.delete_user(user)
    response.delete_cookie(key=sck.SESSION)
    response.delete_cookie(key=sck.DT_EXP)
    return {"message": "Операция выполнена успешно"}
