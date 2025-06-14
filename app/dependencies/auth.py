from typing import Annotated

from fastapi import Cookie, HTTPException
from fastapi.params import Depends
from fastapi.responses import Response
from sqlalchemy.orm import Session

from app.db.database import get_session
from app.enums.app_enums import SessionCookieKey as sck
from app.exceptions.session_exceptions import SessionIsNoneException, SessionIsOldException, SessionDeadException, \
    SessionNotFoundException
from app.exceptions.user_exceptions import UserNotFoundException
from app.schemas.cookie_session import CookieSession
from app.services.app_service import AppService
from app.services.user_service import UserService


def get_current_user(
        cs: Annotated[CookieSession, Cookie()],
        response: Response,
        session: Session = Depends(get_session)
):
    app_service = AppService(session)
    try:
        # Validate session
        app_service.validate_session(cs.session_uuid)
    except SessionIsNoneException as sn:
        raise HTTPException(status_code=sn.status_code, detail=sn.message)
    except SessionIsOldException as so:
        # Refresh session
        new_session = app_service.refresh_session(cs)
        response.set_cookie(key=sck.SESSION.value, value=str(new_session.session_uuid))
        cs = new_session
    except SessionDeadException as sd:
        raise HTTPException(status_code=sd.status_code, detail=sd.message)
    except SessionNotFoundException as snf:
        raise HTTPException(status_code=snf.status_code, detail=snf.message)

    try:
        # Return current user
        user_service = UserService(session)
        return user_service.get_user(uuid_session=cs.session_uuid)
    except UserNotFoundException as nf:
        raise HTTPException(status_code=nf.status_code, detail=nf.message)
