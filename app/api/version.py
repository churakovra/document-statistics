from http import HTTPStatus

from fastapi import APIRouter

from app.enums.app_enums import HandlerTypes
from app.services.app_service import AppService

router = APIRouter()


@router.get(
    path="/version",
    tags=[HandlerTypes.APP],
    response_model=dict[str, str],
    status_code=HTTPStatus.OK,
    summary="Получение версии приложения",
    description="Получение текущей версии приложения",
    responses={
        HTTPStatus.OK: {"description": "Операция успешно выполнена"}
    })
async def get_version():
    version = AppService.get_version()
    return {"version": version}
