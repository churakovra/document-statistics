from sqlalchemy.orm import Session

from app.config.version import __version__
from app.enums.app_enums import Status
from app.repositories.app_repository import AppRepository

from app.config.metrics import METRICS_DESCRIPTION

class AppService:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def check_status(self) -> Status:
        app_repository = AppRepository(self.db_session)
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
