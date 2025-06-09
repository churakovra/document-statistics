from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.orm import Session

from app.db.database import get_session
from app.exceptions.user_exceptions import UserNotFoundException, UserWrongPasswordException
from app.schemas.login_fail_response import LoginFail
from app.schemas.user_login import UserLogin
from app.services.user_service import UserService

router = APIRouter()


@router.post("/login")
async def login(user_creds: UserLogin, session: Session = Depends(get_session)):
    user_service = UserService(session)
    try:
        user_service.auth(user_creds)
    except UserNotFoundException as nf:
        return LoginFail(message=str(nf), status_code=nf.status_code)
    except UserWrongPasswordException as wp:
        return LoginFail(message=str(wp), status_code=wp.status_code)
