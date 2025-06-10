import uuid
from datetime import datetime, timedelta

from sqlalchemy import text
from sqlalchemy.orm import Session

from app.config.preferences import SESSION_ALIVE_HOURS

from app.db.models.user_account import UserAccount
from app.db.models.user_session import UserSession

from app.db.models.document import Document
from app.db.models.collection import Collection
from app.db.models.collection_documents import CollectionDocuments

from app.db.models.statistics import Statistics

from app.schemas.cookie_session import CookieSession
from app.schemas.user_dto import UserDTO


class AppRepository:
    def __init__(self, db_session: Session):
        self.db = db_session

    async def connect_to_db(self):
        try:
            with self.db as session:
                session.execute(text("select 1;"))
            return True
        except Exception:
            return False


    def create_session(self, user: UserDTO) -> CookieSession:
        user_session = UserSession(
            uuid_session=uuid.uuid4(),
            uuid_user=user.uuid,
            dt_exp=datetime.now() + timedelta(hours=SESSION_ALIVE_HOURS)
        )
        self.db.add(user_session)
        self.db.commit()
        self.db.refresh(user_session)
        user_session_reply = CookieSession(
            user_session=str(user_session.uuid_session),
            dt_exp=user_session.dt_exp
        )
        return user_session_reply
