from fastapi import APIRouter
from fastapi import UploadFile
from fastapi.params import Depends
from sqlalchemy.orm import Session
from starlette.requests import Request
from starlette.status import HTTP_200_OK

from app.database import get_session
from app.repositories.file_repository import FileRepository
from app.services.file_service import FileService

router = APIRouter()


# Ендпоинт для обработки загрузки файла
@router.post("/file/new")
async def add_new_file(
        file: UploadFile,
        request: Request,
        session: Session = Depends(get_session)
):
    user_file = await FileService.parse_file(file, request.client.host)
    fid = FileRepository.add_file(user_file, session)
    return {
        "code": HTTP_200_OK,
        "file_name": f"{file.filename}",
        "file_id": f"{fid}"

    }
