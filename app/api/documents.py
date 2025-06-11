from typing import Annotated

from fastapi import APIRouter, HTTPException
from fastapi.params import Depends, Cookie
from fastapi.responses import Response
from sqlalchemy.orm import Session

from app.db.database import get_session
from app.enums.app_enums import SessionCookieKey as sck
from app.exceptions.document_exceptions import DocumentsIsNotFound
from app.exceptions.session_exceptions import SessionIsNoneException, SessionIsOldException
from app.exceptions.user_exceptions import UserNotFoundException
from app.schemas.cookie_session import CookieSession
from app.services.document_service import DocumentService
from app.services.user_service import UserService

router = APIRouter()


@router.get(
    path="/documents"
)
async def get_documents(
        cs: Annotated[CookieSession, Cookie()],
        response: Response,
        session: Session = Depends(get_session)
):
    user_service = UserService(session)
    try:
        user_service.check_session(cs)
    except SessionIsNoneException as sn:
        raise HTTPException(status_code=sn.status_code, detail=sn.message)
    except SessionIsOldException as so:
        new_session = user_service.refresh_session(cs)
        response.set_cookie(key=sck.SESSION.value, value=new_session.user_session)
        response.set_cookie(key=sck.DT_EXP.value, value=str(new_session.dt_exp))
        cs = new_session

    try:
        user = user_service.get_user(uuid_session=cs.user_session)
    except UserNotFoundException as nf:
        raise HTTPException(status_code=nf.status_code, detail=nf.message)

    document_service = DocumentService(session)
    try:
        documents = document_service.get_user_documents(user)
        return documents
    except DocumentsIsNotFound as nf:
        raise HTTPException(status_code=nf.status_code, detail=nf.message)
