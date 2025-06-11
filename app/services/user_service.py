from datetime import datetime
from uuid import UUID

from sqlalchemy.orm import Session

from app.exceptions.session_exceptions import SessionIsNoneException
from app.exceptions.user_exceptions import UserNotFoundException, UserWrongPasswordException, UserAlreadyExistsException
from app.repositories.user_repository import UserRepository
from app.schemas.cookie_session import CookieSession
from app.schemas.new_user import NewUserAccount
from app.schemas.responses.user_account_response import UserCreds
from app.schemas.user_change_password import UserChangePassword
from app.schemas.user_dto import UserDTO
from app.schemas.user_login import UserLogin
from app.services.app_service import AppService
from app.services.auth_service import AuthService


class UserService:
    def __init__(self, session: Session):
        self.db = session

    def get_user(self, **credentials) -> UserDTO | None:
        user_repo = UserRepository(self.db)
        if "username" in credentials:
            username = credentials["username"]
            user = user_repo.get_user(username=username)
            if user is None:
                raise UserNotFoundException(credentials["username"])
        elif "uuid" in credentials:
            uuid = credentials["uuid"]
            user = user_repo.get_user(username=uuid)
            if user is None:
                raise UserNotFoundException(credentials["uuid"])
        else:
            raise ValueError("Требуется указать либо 'username', либо 'uuid'")

    def auth(self, user_creds: UserLogin) -> CookieSession:
        user = self.get_user(username=user_creds.username)
        if user is None:
            raise UserNotFoundException(user_creds.username)
        if not AuthService.validate_pass(user_creds.password, user.password_hashed):
            raise UserWrongPasswordException()
        app_service = AppService(self.db)
        user_session = app_service.create_session(user.uuid)
        return user_session

    def check_session(self, cs: CookieSession):
        if cs.user_session is None:
            raise SessionIsNoneException
        elif cs.dt_exp <= datetime.now():
            app_service = AppService(self.db)
            new_session = app_service.refresh_session(cs)
            return new_session

    def register_user(self, user_creds: NewUserAccount):
        user_repo = UserRepository(self.db)
        if self.get_user(username=user_creds.username) is not None:
            raise UserAlreadyExistsException(user_creds.username)

        password_hashed = AuthService.hash_pass(user_creds.password)
        user_creds.password = password_hashed
        user_repo.add_user(user_creds)
        new_user = self.get_user(username=user_creds.username)
        return UserCreds(
            uuid=new_user.uuid,
            username=new_user.username,
            dt_reg=new_user.dt_reg
        )

    def change_password(self, user_uuid: UUID, ucp: UserChangePassword):
        user_repository = UserRepository(self.db)
        user = self.get_user(uuid=user_uuid)
        if user is None:
            raise UserNotFoundException(str(user_uuid))
        if not AuthService.validate_pass(ucp.password_old, user.password_hashed):
            raise UserWrongPasswordException
        password_hashed_new = AuthService.hash_pass(ucp.password_new)
        user.password_hashed = password_hashed_new
        user_repository.set_new_pass(user)



