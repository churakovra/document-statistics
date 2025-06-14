from http import HTTPStatus

from fastapi import APIRouter

from app.enums.app_enums import HandlerTypes

router = APIRouter()


@router.get(
    path="/",
    tags=[HandlerTypes.APP],
    response_model=dict[str, str],
    status_code=HTTPStatus.OK,
    summary="Приветствие",
    description="Страница приветствия",
    responses={
        HTTPStatus.OK: {"description": "Операция успешно выполнена"}
    }
)
async def root():
    return {"message": "Hi! I'm alive! If you're from Lesta games, welcome!"}
