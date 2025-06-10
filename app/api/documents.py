from typing import Annotated

from fastapi import APIRouter
from fastapi.params import Depends, Cookie
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.db.database import get_session
from app.exceptions.session_exceptions import SessionIsNoneException
from app.schemas.cookie_session import CookieSession
from app.services.user_service import UserService

router = APIRouter()


@router.get("/documents")
async def get_documents(
        cs: Annotated[CookieSession, Cookie()],
        session: Session = Depends(get_session)
):
    user_service = UserService(session)
    try:
        user_service.check_session(cs)
    except SessionIsNoneException as e:
        RedirectResponse(url="/login", status_code=e.status_code)
