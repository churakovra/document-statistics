from fastapi import APIRouter
from fastapi.params import Depends, Query
from sqlalchemy.orm import Session

from app.controllers.get_file_info_from_db_controller import get_file_info_db
from app.database import get_session
from app.models.word_stat_response_model import WordStats

get_file_info_router = APIRouter()


@get_file_info_router.get("/file")
async def get_file_info(
        file_id: int,
        limit: int = Query(50, ge=1, le=100),
        offset: int = Query(default=0, ge=0),
        session: Session = Depends(get_session)) -> list[WordStats]:
    statistics = get_file_info_db(
        file_id=file_id,
        limit=limit,
        offset=offset,
        session=session)
    return statistics
