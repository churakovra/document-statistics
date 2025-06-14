from http import HTTPStatus

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_session
from app.enums.app_enums import HandlerTypes
from app.services.app_service import AppService

router = APIRouter()


@router.get(
    path="/status",
    tags=[HandlerTypes.APP],
    response_model=dict[str, str],
    status_code=HTTPStatus.OK,
    summary="Получение статуса",
    description="Получение статуса работоспособности сервиса",
    responses={
        HTTPStatus.OK: {"description": "Операция успешно выполнена"}
    }
)
async def get_status(session: Session = Depends(get_session)):
    app_service = AppService(session)
    status = app_service.check_status()
    return {"status": status.value}
