from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.models.base import Base
from app.db.models.collection import Collection
from app.db.models.document import Document


class CollectionDocuments(Base):
    __tablename__ = "collection_documents"

    id: Mapped[UUID] = mapped_column(primary_key=True)
    collection_uuid: Mapped[UUID] = mapped_column(ForeignKey("collection.id"), nullable=False)
    document_uuid: Mapped[UUID] = mapped_column(ForeignKey("document.id"), nullable=False)

    collection: Mapped["Collection"] = relationship("Collection", back_populates="documents")
    document: Mapped["Document"] = relationship("Document", back_populates="collections")