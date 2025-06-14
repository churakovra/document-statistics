from datetime import datetime
from typing import List
from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.models.user_account import UserAccount
from app.db.models.base import Base
from app.db.models.collection_documents import CollectionDocuments


class Document(Base):
    __tablename__ = "document"

    uuid: Mapped[UUID] = mapped_column(primary_key=True)
    path: Mapped[str]
    user_load: Mapped[UUID] = mapped_column(ForeignKey("user_account.uuid"), nullable=False)
    dt_load: Mapped[datetime]

    user_account: Mapped["UserAccount"] = relationship("UserAccount", back_populates="documents")
    collections: Mapped[List["CollectionDocuments"]] = relationship("CollectionDocuments", back_populates="document")
