from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.orm import Session

from app.database import get_session

get_file_info_router = APIRouter()


@get_file_info_router.get("/file/{id}")
async def get_file_info(id: int, session: Session = Depends(get_session())):
    pass

