from http import HTTPStatus

from fastapi import APIRouter, Response, HTTPException
from fastapi.params import Depends
from sqlalchemy.orm import Session

from app.db.database import get_session
from app.enums.app_enums import SessionCookieKey as sck, HandlerTypes
from app.exceptions.user_exceptions import UserNotFoundException, UserWrongPasswordException
from app.schemas.user.user_account_response import UserAccountResponse
from app.schemas.user.user_login import UserLogin
from app.services.user_service import UserService

router = APIRouter()


@router.post(
    path="/login",
    tags=[HandlerTypes.USERS],
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
        response.set_cookie(key=sck.SESSION.value, value=user_session.user_session)
        response.set_cookie(key=sck.DT_EXP.value, value=str(user_session.dt_exp))
        return UserAccountResponse(message="Success", status_code=HTTPStatus.OK)
    except UserNotFoundException as nf:
        raise HTTPException(status_code=nf.status_code, detail=nf.message)
    except UserWrongPasswordException as wp:
        raise HTTPException(status_code=wp.status_code, detail=wp.message)
