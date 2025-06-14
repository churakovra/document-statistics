import uuid
from uuid import UUID
from datetime import datetime, timedelta, timezone

from sqlalchemy import text, update, select, and_, delete, desc
from sqlalchemy.orm import Session

from app.config.preferences import SESSION_ALIVE_HOURS

from app.db.models.user_account import UserAccount
from app.db.models.user_session import UserSession

from app.db.models.document import Document
from app.db.models.collection import Collection
from app.db.models.collection_documents import CollectionDocuments

from app.db.models.statistics import Statistics
from app.exceptions.session_exceptions import SessionNotFoundException

from app.schemas.cookie_session import CookieSession
from app.schemas.user.user_session_dto import UserSessionDTO


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

    def create_session(self, user_uuid: uuid.UUID) -> CookieSession:
        user_session = UserSession(
            uuid_session=uuid.uuid4(),
            uuid_user=user_uuid,
            dt_exp=datetime.now(timezone.utc).astimezone() + timedelta(hours=SESSION_ALIVE_HOURS)
        )
        self.db.add(user_session)
        self.db.commit()
        self.db.refresh(user_session)
        user_session_reply = CookieSession(
            session_uuid=user_session.uuid_session
        )
        return user_session_reply

    def get_session(self, *, session_uuid: UUID | None = None, user_uuid: UUID | None = None) -> UserSessionDTO | None:
        if session_uuid:
            stmt = (
                select(UserSession)
                .where(UserSession.uuid_session == session_uuid)
                .order_by(desc(UserSession.dt_exp))
            )
        elif user_uuid:
            stmt = (
                select(UserSession)
                .where(UserSession.uuid_user == user_uuid)
                .order_by(desc(UserSession.dt_exp))
            )
        else:
            raise ValueError("Нужно передать или session_uuid или user_uuid")
        user_session = self.db.scalar(stmt)
        if user_session is None:
            return user_session
        session_dto = UserSessionDTO(
            uuid_session=user_session.uuid_session,
            uuid_user=user_session.uuid_user,
            dt_exp=user_session.dt_exp,
            alive=user_session.alive
        )
        return session_dto

    def deactivate_session(self, cs: CookieSession):
        session = self.get_session(session_uuid=cs.session_uuid)
        if session is None:
            raise SessionNotFoundException(cs.session_uuid)
        if not session.alive:
            return session
        stmt = (
            update(UserSession)
            .where(UserSession.uuid_session == cs.session_uuid)
            .values(alive=False)
        )
        self.db.execute(stmt)
        self.db.commit()
        return session

    def deactivate_user_sessions(self, user_uuid: UUID):
        stmt = (
            update(UserSession)
            .where(
                and_(
                    UserSession.uuid_user == user_uuid,
                    UserSession.alive == True
                )
            )
            .values(alive=False)
        )
        self.db.execute(stmt)
        self.db.commit()

    def delete_user_sessions(self, user_uuid: UUID):
        stmt = delete(UserSession).where(UserSession.uuid_user == user_uuid)
        self.db.execute(stmt)
        self.db.commit()
