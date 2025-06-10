from sqlalchemy.orm import Session

from app.config.metrics import METRICS_DESCRIPTION
from app.config.version import __version__
from app.enums.app_enums import Status
from app.repositories.app_repository import AppRepository
from app.schemas.cookie_session import CookieSession
from app.schemas.user_dto import UserDTO


class AppService:
    def __init__(self, db_session: Session):
        self.db = db_session

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

    def get_session(self, user: UserDTO) -> CookieSession:
        app_repository = AppRepository(self.db)
        user_session = app_repository.create_session(user)
        return user_session
