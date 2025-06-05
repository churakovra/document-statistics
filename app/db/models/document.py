from datetime import datetime
from typing import List
from uuid import UUID

from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.models.base import Base
from app.db.models.collection_documents import CollectionDocuments


class Document(Base):
    __tablename__ = "document"

    id: Mapped[UUID] = mapped_column(primary_key=True)
    path: Mapped[str]
    load_user: Mapped[UUID]
    load_dt: Mapped[datetime]

    collections: Mapped[List["CollectionDocuments"]] = relationship("CollectionDocuments", back_populates="document")
