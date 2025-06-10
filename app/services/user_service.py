from datetime import datetime

from sqlalchemy.orm import Session

from app.exceptions.session_exceptions import SessionIsNoneException
from app.exceptions.user_exceptions import UserNotFoundException, UserWrongPasswordException
from app.repositories.user_repository import UserRepository
from app.schemas.cookie_session import CookieSession
from app.schemas.user_login import UserLogin
from app.services.app_service import AppService
from app.services.auth_service import AuthService


class UserService:
    def __init__(self, session: Session):
        self.session = session

    def auth(self, user_creds: UserLogin) -> CookieSession:
        user_repo = UserRepository(self.session)
        user = user_repo.get_user(user_creds.username)
        if user is None:
            raise UserNotFoundException
        if not AuthService.validate_pass(user_creds.password, user.password_hashed):
            raise UserWrongPasswordException()
        app_service = AppService(self.session)
        user_session = app_service.get_session(user)
        return user_session

    def check_session(self, cs: CookieSession):
        if cs.user_session is None:
            raise SessionIsNoneException
        elif cs.dt_exp <= datetime.now():
            self.refresh(cs)

    def refresh(self, cs: CookieSession):
        pass
