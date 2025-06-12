from datetime import datetime
from typing import List
from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.models.base import Base
from app.db.models.collection_documents import CollectionDocuments
from app.db.models.user_account import UserAccount


class Collection(Base):
    __tablename__ = "collection"

    uuid: Mapped[UUID] = mapped_column(primary_key=True)
    user_create: Mapped[UUID] = mapped_column(ForeignKey("user_account.uuid"), nullable=False)
    dt_create: Mapped[datetime]
    base: Mapped[bool] = mapped_column(default=False)

    user_account: Mapped["UserAccount"] = relationship("UserAccount", back_populates="collections")
    documents: Mapped[List["CollectionDocuments"]] = relationship("CollectionDocuments", back_populates="collection")
