from sqlalchemy import select, func
from sqlalchemy.orm import Session

from app.schemas.user_file_dto import UserFileDTO


class FileRepository:
    @staticmethod
    # Добавляем файл в БД + добавляем слова
    def add_file(file: UserFileDTO, session: Session) -> int:
        user_file = UserFile(
            file_name=file.file_name,
            file_size=file.file_size,
            load_datetime=file.load_datetime,
            user=file.user
        )
        session.add(user_file)
        session.commit()
        session.refresh(user_file)

        FileRepository.add_file_words(user_file.id, file, session)

        session.commit()
        return user_file.id

    @staticmethod
    # Добавляем в file_words слово + файл
    def add_file_words(user_file_id: int, file: UserFileDTO, session: Session):
        for word in file.words:
            user_word = FileRepository.add_word(UserWord(word=word), session)

            file_word = FileWord(
                id_file=user_file_id,
                id_word=user_word.id
            )
            session.add(file_word)
            session.commit()
            session.refresh(file_word)

    @staticmethod
    def add_word(word: UserWord, session: Session) -> UserWord:
        stmt = select(UserWord).where(UserWord.word == word.word)
        result = session.execute(stmt)
        exists = result.scalars().first()
        if exists:
            return exists
        session.add(word)
        session.commit()
        session.refresh(word)
        return word

    @staticmethod
    def get_words(file_id: int, session: Session):
        return session.execute(
            select(
                UserWord.word,
                func.count(FileWord.id_word)
            )
            .join(UserWord, FileWord.id_word == UserWord.id)
            .where(FileWord.id_file == file_id)
            .group_by(FileWord.id_word, UserWord.word)
            .order_by(FileWord.id_word.desc())
        ).all()

    @staticmethod
    def get_word_in_files(file_id: int, session: Session):
        return session.execute(
            select(
                func.count(FileWord.id_file.distinct())
            )
            .where(
                FileWord.id_word.in_(
                    select(
                        FileWord.id_word
                    )
                    .where(FileWord.id_file == file_id)
                )
            )
            .group_by(FileWord.id_word)
            .order_by(FileWord.id_word.desc())
        ).all()

    @staticmethod
    def get_file_size(file_id: int, session: Session) -> int:
        return session.scalar(
            select(
                UserFile.file_size
            )
            .where(UserFile.id == file_id)
            .group_by(UserFile.file_size)
        )

    @staticmethod
    def get_files_count(file_id: int, session: Session) -> int:
        return session.scalar(
            select(
                func.count(UserFileDTO.id)
            )
            .where(UserFile.id == file_id)
        )
