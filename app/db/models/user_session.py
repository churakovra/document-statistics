from datetime import datetime
from uuid import UUID

from sqlalchemy import ForeignKey, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.models.base import Base
from app.db.models.user_account import UserAccount


class UserSession(Base):
    __tablename__ = "user_session"

    uuid_session: Mapped[UUID] = mapped_column(primary_key=True)
    uuid_user: Mapped[UUID] = mapped_column(ForeignKey("user_account.uuid"), nullable=False)
    dt_exp: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    alive: Mapped[bool] = mapped_column(default=True)

    user_account: Mapped["UserAccount"] = relationship("UserAccount", back_populates="session")
