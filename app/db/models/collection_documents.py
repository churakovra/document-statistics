from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.models.base import Base

if TYPE_CHECKING:
    from app.db.models.collection import Collection
    from app.db.models.document import Document


class CollectionDocuments(Base):
    __tablename__ = "collection_documents"

    uuid: Mapped[UUID] = mapped_column(primary_key=True)
    uuid_collection: Mapped[UUID] = mapped_column(ForeignKey("collection.uuid"), nullable=False)
    uuid_document: Mapped[UUID] = mapped_column(ForeignKey("document.uuid"), nullable=False)
    dt_add: Mapped[datetime]

    collection: Mapped["Collection"] = relationship("Collection", back_populates="documents")
    document: Mapped["Document"] = relationship("Document", back_populates="collections")
