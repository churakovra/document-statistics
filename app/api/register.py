from http import HTTPStatus

from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from sqlalchemy.orm import Session

from app.db.database import get_session
from app.enums.app_enums import HandlerTypes as ht
from app.exceptions.user_exceptions import UserAlreadyExistsException
from app.schemas.new_user import NewUserAccount
from app.schemas.responses.user_account_response import UserAccountResponse
from app.services.user_service import UserService

router = APIRouter()


@router.post(
    "/register",
    tags=[ht.USER],
    response_model=UserAccountResponse,
    status_code=HTTPStatus.CREATED,
    summary="Регистрация нового пользователя",
    description="Создаёт нового пользователя в системе. В случае, если пользователь уже существует, возвращает ошибку.",
    responses={
        HTTPStatus.CREATED: {"description": "Пользователь успешно зарегистрирован"},
        HTTPStatus.CONFLICT: {"description": "Пользователь с таким email уже существует"},
    }
)
async def register(
        new_usr: NewUserAccount,
        session: Session = Depends(get_session),
):
    try:
        user_service = UserService(session)
        user_service.register_user(new_usr)
        return UserAccountResponse(message="Success!", status_code=HTTPStatus.CREATED)
    except UserAlreadyExistsException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
