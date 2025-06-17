from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy.orm import Session

from app.config.metrics import METRICS_DESCRIPTION
from app.config.version import __version__
from app.enums.app_enums import Status
from app.exceptions.session_exceptions import SessionNotFoundException, SessionIsNoneException, SessionIsOldException, \
    SessionDeadException
from app.exceptions.user_exceptions import UserWrongPasswordException
from app.repositories.app_repository import AppRepository
from app.schemas.cookie_session import CookieSession
from app.schemas.user.user_dto import UserDTO
from app.schemas.user.user_login import UserLogin
from app.schemas.user.user_session_dto import UserSessionDTO
from app.services.security_service import SecurityService


class AppService:
    def __init__(self, db_session: Session):
        self.db = db_session

    def auth(self, user: UserDTO, user_creds: UserLogin) -> CookieSession:
        if not SecurityService.validate_pass(user_creds.password, user.password_hashed):
            raise UserWrongPasswordException()
        user_session = self.create_session(user.uuid)
        return user_session

    def create_session(self, user_uuid: UUID) -> CookieSession:
        try:
            user_session = self.get_user_session(user_uuid)
            self.validate_session(user_session.uuid_session)
            return CookieSession(session_uuid=user_session.uuid_session)
        except (SessionNotFoundException, SessionIsOldException, SessionDeadException):
            app_repository = AppRepository(self.db)
            user_session = app_repository.create_session(user_uuid)
        return user_session

    def validate_session(self, session_uuid: UUID):
        if len(str(session_uuid)) <= 0:
            raise SessionIsNoneException()
        session = self.get_session(session_uuid)
        if session.dt_exp <= datetime.now(timezone.utc).astimezone():
            raise SessionIsOldException(session.uuid_session)
        if not session.alive:
            raise SessionDeadException(session.uuid_session)

    def get_session(self, session_uuid: UUID) -> UserSessionDTO:
        app_repository = AppRepository(self.db)
        session = app_repository.get_session(session_uuid=session_uuid)
        if session is None:
            raise SessionNotFoundException(session_uuid)
        return session

    def get_user_session(self, user_uuid: UUID) -> UserSessionDTO:
        app_repository = AppRepository(self.db)
        session = app_repository.get_session(user_uuid=user_uuid)
        if session is None:
            raise SessionNotFoundException(f"for user {user_uuid}")
        return session

    def refresh_session(self, cs: CookieSession) -> CookieSession:
        old_session = self.deactivate_session(cs)
        new_session = self.create_session(old_session.uuid_user)
        return new_session

    def deactivate_session(self, cs: CookieSession) -> UserSessionDTO:
        app_repository = AppRepository(self.db)
        return app_repository.deactivate_session(cs)

    def deactivate_user_sessions(self, user_uuid: UUID):
        app_repository = AppRepository(self.db)
        app_repository.deactivate_user_sessions(user_uuid)

    def delete_user_sessions(self, user_uuid: UUID):
        app_repository = AppRepository(self.db)
        app_repository.delete_user_sessions(user_uuid)

    def check_status(self) -> Status:
        app_repository = AppRepository(self.db)
        db_up = app_repository.connect_to_db()
        if db_up:
            return Status.OK
        return Status.ERROR

    @staticmethod
    def get_version() -> str:
        version = __version__
        return version

    @staticmethod
    def get_metrics() -> dict[str, str]:
        return METRICS_DESCRIPTION
