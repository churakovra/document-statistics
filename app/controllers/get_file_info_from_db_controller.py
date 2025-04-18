from math import log

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.user_files_db_model import UserFiles
from app.models.user_words_db_model import UserWords
from app.models.word_stat_response_model import WordStats
from app.models.words_in_file_db_model import FileWords


def get_file_info_db(file_id: int, session: Session) -> list[WordStats]:
    res = list()

    words_in_file = session.execute(
        select(
            UserWords.word,
            func.count(FileWords.id_word)
        )
        .join(UserWords, FileWords.id_word == UserWords.id)
        .where(FileWords.id_file == file_id)
        .group_by(FileWords.id_word, UserWords.word)
        .order_by(FileWords.id_word.desc())
    ).all()

    word_in_files_query = session.execute(
        select(
            func.count(FileWords.id_file.distinct())
        )
        .where(
            FileWords.id_word.in_(
                select(
                    FileWords.id_word
                )
                .where(FileWords.id_file == file_id)
            )
        )
        .group_by(FileWords.id_word)
        .order_by(FileWords.id_word.desc())
    ).all()

    file_size = session.scalar(
        select(
            UserFiles.file_size
        )
        .where(UserFiles.id == file_id)
        .group_by(UserFiles.file_size)
    )

    files_count = session.scalar(
        select(
            func.count(UserFiles.id)
        )
        .where(UserFiles.id == file_id)
    )

    for _ in range(0, len(words_in_file)):
        word, words_in_file_count = words_in_file[_]
        file_count = word_in_files_query[_][0]
        res.append(
            WordStats(
                word=word,
                words_in_file_count=words_in_file_count,
                file_size=file_size,
                file_count=file_count,
                files_count=files_count,
                tf=words_in_file_count / file_size,
                idf=log(files_count / file_count)
            )
        )

    return res
