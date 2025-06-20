import uuid
from datetime import datetime
from uuid import UUID

from sqlalchemy import select, and_, delete
from sqlalchemy.orm import Session

from app.db.models.user_account import UserAccount
from app.db.models.user_session import UserSession

from app.db.models.document import Document
from app.db.models.collection import Collection
from app.db.models.collection_documents import CollectionDocuments

from app.db.models.statistics import Statistics
from app.exceptions.collection_exceptions import BaseCollectionNotFoundException
from app.schemas.collection.collection_dto import CollectionDTO


class CollectionRepository:
    def __init__(self, session: Session):
        self.db = session

    def create_collection(
            self,
            user_uuid: UUID,
            label: str,
            base: bool = False,
    ) -> CollectionDTO:
        new_collection = Collection(
            uuid=uuid.uuid4(),
            label=label,
            user_create=user_uuid,
            dt_create=datetime.now(),
            base=base
        )

        self.db.add(new_collection)
        self.db.commit()
        self.db.refresh(new_collection)

        new_collection_dto = CollectionDTO(
            uuid=new_collection.uuid,
            label=new_collection.label,
            user_create=new_collection.user_create,
            dt_create=new_collection.dt_create,
            base=new_collection.base
        )
        return new_collection_dto

    def add_document_to_collection(self, collection_uuid: UUID, document_uuid: UUID) -> UUID:
        collection_document = CollectionDocuments(
            uuid=uuid.uuid4(),
            uuid_collection=collection_uuid,
            uuid_document=document_uuid,
            dt_add=datetime.now()
        )
        self.db.add(collection_document)
        self.db.commit()
        self.db.refresh(collection_document)
        return collection_document.uuid

    def add_document_to_base_collection(self, document_uuid: UUID, user_uuid: UUID) -> UUID:
        collection = self.get_base_collection(user_uuid)
        if collection is None:
            BaseCollectionNotFoundException(user_uuid)
        return self.add_document_to_collection(collection_uuid=collection.uuid, document_uuid=document_uuid)

    def get_collection(self, collection_uuid: UUID) -> CollectionDTO | None:
        stmt = select(Collection).where(Collection.uuid == collection_uuid)
        collection = self.db.scalar(stmt)
        if collection is None:
            return collection
        return CollectionDTO(
            uuid=collection.uuid,
            label=collection.label,
            user_create=collection.user_create,
            dt_create=collection.dt_create,
            base=collection.base
        )

    def get_collections(self, user_uuid: UUID) -> list[CollectionDTO]:
        stmt = (
            select(Collection)
            .where(
                Collection.user_create == user_uuid
            )
        )
        collections = list[CollectionDTO]()
        for collection in self.db.scalars(stmt):
            collections.append(
                CollectionDTO(
                    uuid=collection.uuid,
                    label=collection.label,
                    user_create=collection.user_create,
                    dt_create=collection.dt_create,
                    base=collection.base
                )
            )
        return collections

    def get_base_collection(self, user_uuid: UUID) -> CollectionDTO | None:
        stmt = (
            select(Collection)
            .where(
                and_(
                    Collection.user_create == user_uuid,
                    Collection.base == True
                )
            )
        )
        collection = self.db.scalar(stmt)
        if collection is None:
            return collection
        collection_dto = CollectionDTO(
            uuid=collection.uuid,
            label=collection.label,
            user_create=collection.user_create,
            dt_create=collection.dt_create,
            base=collection.base
        )
        return collection_dto

    def get_collection_document(self, collection_uuid: UUID, document_uuid: UUID) -> UUID | None:
        stmt = (
            select(CollectionDocuments.uuid_document)
            .where(
                and_(
                    CollectionDocuments.uuid_collection == collection_uuid,
                    CollectionDocuments.uuid_document == document_uuid
                )
            )
        )
        collection_uuid = self.db.scalar(stmt)
        return collection_uuid

    def get_collection_documents(self, collection_uuid: UUID) -> list[UUID]:
        stmt = select(CollectionDocuments.uuid_document).where(CollectionDocuments.uuid_collection == collection_uuid)
        documents = list[UUID]()
        for document_uuid in self.db.scalars(stmt):
            documents.append(document_uuid)
        return documents

    def remove_document(self, document_uuid: UUID):
        stmt = delete(CollectionDocuments).where(CollectionDocuments.uuid_document == document_uuid)
        self.db.execute(stmt)
        self.db.commit()

    def remove_document_from_collection(self, collection_uuid: UUID, document_uuid: UUID):
        stmt = (
            delete(CollectionDocuments)
            .where(
                and_(
                    CollectionDocuments.uuid_collection == collection_uuid,
                    CollectionDocuments.uuid_document == document_uuid
                )
            )
        )
        self.db.execute(stmt)
        self.db.commit()

    def remove_documents_from_collection(self, collection_uuid: UUID):
        stmt = delete(CollectionDocuments).where(CollectionDocuments.uuid_collection == collection_uuid)
        self.db.execute(stmt)
        self.db.commit()

    def delete_collection(self, collection_uuid: UUID):
        stmt = delete(Collection).where(Collection.uuid == collection_uuid)
        self.db.execute(stmt)
        self.db.commit()
