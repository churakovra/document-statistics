import string
from datetime import datetime
from math import log

from fastapi import UploadFile
from sqlalchemy.orm import Session

from app.schemas.user_file_dto import UserFileDTO
from app.schemas.word_stat_dto import WordStatDTO
from app.repositories.file_repository import FileRepository


class FileService:
    @staticmethod
    async def parse_file(file: UploadFile, user_host: str) -> UserFileDTO:
        content = (await file.read()).decode("utf-8")  # Читаем файл
        words = [word.strip(string.punctuation).lower() for word in content.split()]
        user_file = UserFileDTO(
            file_name=file.filename,
            file_size=len(words),
            load_datetime=datetime.now(),
            user=user_host,
            words=words
        )
        return user_file

    @staticmethod
    def get_file_info(
            file_id: int,
            limit: int,
            offset: int,
            session: Session
    ) -> list[WordStatDTO]:
        pre_res = list[WordStatDTO]()
        words_in_file = FileRepository.get_words(file_id, session)
        word_in_files_query = FileRepository.get_word_in_files(file_id, session)
        file_size = FileRepository.get_file_size(file_id, session)
        files_count = FileRepository.get_files_count(file_id, session)

        for _ in range(0, len(words_in_file)):
            word, words_in_file_count = words_in_file[_]
            file_count = word_in_files_query[_][0]
            pre_res.append(
                WordStatDTO(
                    word=word,
                    words_in_file_count=words_in_file_count,
                    file_size=file_size,
                    file_count=file_count,
                    files_count=files_count,
                    tf=words_in_file_count / file_size,
                    idf=log(files_count / file_count, 10)
                )
            )
        pre_res.sort(reverse=True)
        res = list[WordStatDTO]()
        for _ in range(0, limit):
            res.append(pre_res[offset + _])
        return res
