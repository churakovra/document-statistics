import uuid
from datetime import datetime

from sqlalchemy import select, update, delete
from sqlalchemy.orm import Session

from app.db.models.user_account import UserAccount
from app.db.models.user_session import UserSession

from app.db.models.document import Document
from app.db.models.collection import Collection
from app.db.models.collection_documents import CollectionDocuments

from app.db.models.statistics import Statistics

from app.schemas.user.new_user import NewUserAccount
from app.schemas.user.user_dto import UserDTO


class UserRepository:
    def __init__(self, session: Session):
        self.db = session

    def get_user(self, **credentials) -> UserDTO | None:
        if "username" in credentials:
            username = credentials["username"]
            stmt = select(UserAccount).where(UserAccount.username == username)
        elif "uuid" in credentials:
            user_uuid = credentials["uuid"]
            stmt = select(UserAccount).where(UserAccount.uuid == user_uuid)
        elif "uuid_session" in credentials:
            uuid_session = credentials["uuid_session"]
            stmt = (
                select(UserAccount)
                .join(UserSession, UserAccount.uuid == UserSession.uuid_user)
                .where(UserSession.uuid_session == uuid_session)
            )
        else:
            raise ValueError("Требуется указать либо 'username', либо 'uuid'")
        user_account = self.db.scalar(stmt)
        if user_account is None:
            return user_account
        user_dto = UserDTO(
            uuid=user_account.uuid,
            username=user_account.username,
            password_hashed=user_account.password_hashed,
            dt_reg=user_account.dt_reg
        )
        return user_dto

    def add_user(self, user: NewUserAccount):
        user_account = UserAccount(
            uuid=uuid.uuid4(),
            username=user.username,
            password_hashed=user.password,
            dt_reg=datetime.now()
        )
        self.db.add(user_account)
        self.db.commit()
        self.db.refresh(user_account)

    def set_new_pass(self, user: UserDTO):
        stmt = (
            update(UserAccount)
            .where(UserAccount.uuid == user.uuid)
            .values(password_hashed=user.password_hashed)
        )
        self.db.execute(stmt)
        self.db.commit()

    def delete_user(self, user_uuid: uuid.UUID):
        stmt = delete(UserAccount).where(UserAccount.uuid == user_uuid)
        self.db.execute(stmt)
        self.db.commit()
