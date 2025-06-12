import uuid
from datetime import datetime
from uuid import UUID

from sqlalchemy import select, and_
from sqlalchemy.orm import Session

from app.db.models.user_account import UserAccount
from app.db.models.user_session import UserSession

from app.db.models.document import Document
from app.db.models.collection import Collection
from app.db.models.collection_documents import CollectionDocuments

from app.db.models.statistics import Statistics
from app.exceptions.collection_exceptions import BaseCollectionNotFoundException
from app.schemas.collection_dto import CollectionDTO


class CollectionRepository:
    def __init__(self, session: Session):
        self.db = session

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
            user_create=collection.user_create,
            dt_create=collection.dt_create,
            base=collection.base
        )
        return collection_dto

    def create_collection(self, user_uuid: UUID, base: bool = False) -> CollectionDTO:
        if base:
            new_collection = Collection(
                uuid=uuid.uuid4(),
                user_create=user_uuid,
                dt_create=datetime.now(),
                base=base
            )
        else:
            new_collection = Collection(
                uuid=uuid.uuid4(),
                user_create=user_uuid,
                dt_create=datetime.now()
            )
        self.db.add(new_collection)
        self.db.commit()
        self.db.refresh(new_collection)
        new_collection_dto = CollectionDTO(
            uuid=new_collection.uuid,
            user_create=new_collection.user_create,
            dt_create=new_collection.dt_create,
            base=new_collection.base
        )
        return new_collection_dto

    def add_document_to_collection(self, document_uuid: UUID, collection_uuid: UUID) -> UUID:
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
            BaseCollectionNotFoundException()
        return self.add_document_to_collection(document_uuid, collection.uuid)
