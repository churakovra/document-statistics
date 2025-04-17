import string
from datetime import datetime

from fastapi import APIRouter
from fastapi import UploadFile
from fastapi.params import Depends
from sqlalchemy.orm import Session
from starlette.requests import Request
from starlette.status import HTTP_200_OK

from app.controllers.add_new_file_to_db_controller import add_new_file_to_db
from app.database import get_session
from app.models.user_file_model import UserFile

add_new_file_router = APIRouter()


# Ендпоинт для обработки загрузки файла
@add_new_file_router.post("/file/new")
async def add_new_file(
        file: UploadFile,
        request: Request,
        session: Session = Depends(get_session)
):
    content = (await file.read()).decode("utf-8")  # Читаем файл
    words = [word.strip(string.punctuation).lower() for word in content.split()]
    user_file = UserFile(
        file_name=file.filename,
        file_size=len(words),
        load_datetime=datetime.now(),
        user=request.client.host,
        words=words
    )
    add_new_file_to_db(user_file, session) # Отправляем файл в метод для добавления в БД
    return {"message": f"Success! File {file.filename} uploaded, status {HTTP_200_OK}"}
