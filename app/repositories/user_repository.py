from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models.user_account import UserAccount
from app.schemas.user_dto import UserDTO


class UserRepository:
    def __init__(self, session: Session):
        self.db = session

    def get_user(self, username: str) -> UserDTO | None:
        stmt = select(UserAccount).where(UserAccount.username == username)
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
