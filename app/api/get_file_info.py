from fastapi import APIRouter
from fastapi.params import Depends, Query
from sqlalchemy.orm import Session

from app.database import get_session
from app.models.word_stat_response_model import WordStats
from app.services.file_service import FileService

router = APIRouter()


@router.get("/file")
async def get_file_info(
        file_id: int,
        limit: int = Query(50, ge=1, le=100),
        offset: int = Query(default=0, ge=0),
        session: Session = Depends(get_session)
) -> list[WordStats]:
    statistics = FileService.get_file_info(file_id, limit, offset, session)
    return statistics
