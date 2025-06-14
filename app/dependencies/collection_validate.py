from uuid import UUID

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_session
from app.exceptions.collection_exceptions import CollectionNotFoundException
from app.services.collection_service import CollectionService


def validate_collection(
        collection_id: UUID,
        session: Session = Depends(get_session)
):
    collection_service = CollectionService(session)
    try:
        collection = collection_service._get_collection(collection_id)
        return collection.uuid
    except CollectionNotFoundException as nf:
        raise HTTPException(status_code=nf.status_code, detail=nf.message)
