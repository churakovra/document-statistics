from uuid import UUID

from sqlalchemy.orm import Session

from app.config.metrics import METRICS_DESCRIPTION
from app.config.version import __version__
from app.enums.app_enums import Status
from app.repositories.app_repository import AppRepository
from app.schemas.cookie_session import CookieSession
from app.schemas.user.user_session_dto import UserSessionDTO


class AppService:
    def __init__(self, db_session: Session):
        self.db = db_session

    def check_status(self) -> Status:
        app_repository = AppRepository(self.db)
        db_up = app_repository.connect_to_db()
        if db_up:
            return Status.OK
        return Status.ERROR

    def create_session(self, user_uuid: UUID) -> CookieSession:
        app_repository = AppRepository(self.db)
        user_session = app_repository.create_session(user_uuid)
        return user_session

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

    @staticmethod
    def get_version() -> str:
        version = __version__
        return version

    @staticmethod
    def get_metrics() -> dict[str, str]:
        return METRICS_DESCRIPTION
