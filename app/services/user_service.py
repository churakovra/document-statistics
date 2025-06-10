from datetime import datetime

from sqlalchemy.orm import Session

from app.exceptions.session_exceptions import SessionIsNoneException
from app.exceptions.user_exceptions import UserNotFoundException, UserWrongPasswordException, UserAlreadyExistsException
from app.repositories.user_repository import UserRepository
from app.schemas.cookie_session import CookieSession
from app.schemas.new_user import NewUserAccount
from app.schemas.user_login import UserLogin
from app.services.app_service import AppService
from app.services.auth_service import AuthService


class UserService:
    def __init__(self, session: Session):
        self.db = session

    def auth(self, user_creds: UserLogin) -> CookieSession:
        user_repo = UserRepository(self.db)
        user = user_repo.get_user(user_creds.username)
        if user is None:
            raise UserNotFoundException(user_creds.username)
        if not AuthService.validate_pass(user_creds.password, user.password_hashed):
            raise UserWrongPasswordException()
        app_service = AppService(self.db)
        user_session = app_service.get_session(user)
        return user_session

    def check_session(self, cs: CookieSession):
        if cs.user_session is None:
            raise SessionIsNoneException
        elif cs.dt_exp <= datetime.now():
            self.refresh(cs)

    def refresh(self, cs: CookieSession):
        pass

    def register_user(self, user_creds: NewUserAccount):
        user_repo = UserRepository(self.db)
        if user_repo.get_user(user_creds.username) is not None:
            raise UserAlreadyExistsException(user_creds.username)

        password_hashed = AuthService.hash_pass(user_creds.password)
        user_creds.password = password_hashed
        user_repo.add_user(user_creds)
