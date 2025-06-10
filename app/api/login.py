from http import HTTPStatus

from fastapi import APIRouter, Response
from fastapi.params import Depends
from sqlalchemy.orm import Session

from app.config.preferences import DT_STR_FORMAT
from app.db.database import get_session
from app.enums.app_enums import SessionCookieKey as sck
from app.exceptions.user_exceptions import UserNotFoundException, UserWrongPasswordException
from app.schemas.responses.user_account_response import UserAccountResponse
from app.schemas.user_login import UserLogin
from app.services.user_service import UserService

router = APIRouter()


@router.post("/login")
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
