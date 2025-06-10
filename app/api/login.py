from http import HTTPStatus

from fastapi import APIRouter, Response, HTTPException
from fastapi.params import Depends
from sqlalchemy.orm import Session

from app.config.preferences import DT_STR_FORMAT
from app.db.database import get_session
from app.enums.app_enums import SessionCookieKey as sck, HandlerTypes
from app.exceptions.user_exceptions import UserNotFoundException, UserWrongPasswordException
from app.schemas.responses.user_account_response import UserAccountResponse
from app.schemas.user_login import UserLogin
from app.services.user_service import UserService

router = APIRouter()


@router.post(
    path="/login",
    tags=[HandlerTypes.USER],
    response_model=UserAccountResponse,
    status_code=HTTPStatus.OK,
    summary="Аутентификация пользователя",
    description="Проверка кредов с последующим созданием сессии если проверка пройдена",
    responses={
        HTTPStatus.OK: {"description": "Аутентификация успешна"},
        HTTPStatus.NOT_FOUND: {"description": "Пользователь с указанным логином не найден"},
        HTTPStatus.BAD_REQUEST: {"description": "Неверный пароль"}
    }
)
async def login(
        user_creds: UserLogin,
        response: Response,
        session: Session = Depends(get_session),
):
    user_service = UserService(session)
    try:
        user_session = user_service.auth(user_creds)
        response.set_cookie(key=sck.SESSION, value=user_session.user_session)
        response.set_cookie(key=sck.DT_EXP, value=user_session.dt_exp.strftime(DT_STR_FORMAT))
        return UserAccountResponse(message="Success", status_code=HTTPStatus.OK)
    except UserNotFoundException as nf:
        return UserAccountResponse(message=str(nf), status_code=nf.status_code)
    except UserWrongPasswordException as wp:
        return UserAccountResponse(message=str(wp), status_code=wp.status_code)
