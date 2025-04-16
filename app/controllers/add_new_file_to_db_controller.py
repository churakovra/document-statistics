from sqlalchemy.orm import Session

from app.controllers.add_words_from_new_file_to_db import add_words
from app.models.file_contents_db_model import FileContents
from app.models.user_file import UserFile
from app.models.user_file_db_model import UserFile as UserFileDB


async def add_new_file_to_db(file: UserFile, session: Session):
    words = [FileContents(word=word) for word in file.words]
    file_db = UserFileDB(
        file_name=file.file_name,
        load_datetime=file.load_datetime,
        user=file.user,
        words=words
    )
    session.add(file_db)
    session.commit()
    await add_words(words, session)
