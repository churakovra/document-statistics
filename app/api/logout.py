from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, HTTPException
from fastapi.params import Depends, Cookie
from sqlalchemy.orm import Session
from starlette.responses import Response

from app.db.database import get_session
from app.enums.app_enums import SessionCookieKey as sck, HandlerTypes
from app.exceptions.session_exceptions import SessionNotFoundException
from app.schemas.cookie_session import CookieSession
from app.schemas.user.user_account_response import UserAccountResponse
from app.services.app_service import AppService

router = APIRouter()


@router.get(
    path="/logout",
    tags=[HandlerTypes.USER],
    response_model=UserAccountResponse,
    status_code=HTTPStatus.OK,
    summary="Завершение сессии пользователя",
    description="Завершение сессии пользователя, удаление кук авторизации",
    responses={
        HTTPStatus.OK: {"description" : "Сессия успешно завершена"},
        HTTPStatus.NOT_FOUND: {"description": "Сессия не найдена"}
    }
)

async def logout(
        cs: Annotated[CookieSession, Cookie()],
        response: Response,
        session: Session = Depends(get_session),
):
    app_service = AppService(session)
    try:
        app_service.deactivate_session(cs)
        response.delete_cookie(sck.SESSION)
        response.delete_cookie(sck.DT_EXP)
        return UserAccountResponse(message="Сессия успешно завершена", status_code=HTTPStatus.OK)
    except SessionNotFoundException as snf:
        raise HTTPException(status_code=snf.status_code, detail=snf.message)
