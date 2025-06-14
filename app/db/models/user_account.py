from datetime import datetime
from typing import List, TYPE_CHECKING
from uuid import UUID

from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.models.base import Base

if TYPE_CHECKING:
    from app.db.models.collection import Collection
    from app.db.models.document import Document
    from app.db.models.user_session import UserSession


class UserAccount(Base):
    __tablename__ = "user_account"

    uuid: Mapped[UUID] = mapped_column(primary_key=True)
    username: Mapped[str]
    password_hashed: Mapped[str]
    dt_reg: Mapped[datetime]

    documents: Mapped[List["Document"]] = relationship("Document", back_populates="user_account")
    collections: Mapped[List["Collection"]] = relationship("Collection", back_populates="user_account")
    session: Mapped["UserSession"] = relationship("UserSession", back_populates="user_account")
