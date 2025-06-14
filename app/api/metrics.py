from http import HTTPStatus

from fastapi import APIRouter

from app.enums.app_enums import HandlerTypes
from app.services.app_service import AppService

router = APIRouter()


@router.get(
    path="/metrics",
    tags=[HandlerTypes.APP],
    response_model=dict[str, str],
    status_code=HTTPStatus.OK,
    summary="Получение описания метрик приложения",
    description="Получение описания существующих метрик приложения",
    responses={
        HTTPStatus.OK: {"description": "Операция успешно выполнена"}
    }
)
async def get_metrics():
    metrics = AppService.get_metrics()
    return metrics
