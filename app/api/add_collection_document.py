from http import HTTPStatus
from uuid import UUID

from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from sqlalchemy.orm import Session

from app.db.database import get_session
from app.dependencies.auth import get_current_user
from app.dependencies.collection_validate import validate_collection
from app.dependencies.document_validate import validate_document
from app.enums.app_enums import HandlerTypes
from app.exceptions.collection_exceptions import CollectionAlreadyHasDocumentException
from app.schemas.user.user_dto import UserDTO
from app.services.collection_service import CollectionService

router = APIRouter()


@router.post(
    path="/collections/{collection_id}/{document_id}",
    tags=[HandlerTypes.COLLECTIONS],
    status_code=HTTPStatus.OK,
    summary="Добавить документ в коллекцию",
    description="Документ(один и тот же uuid) может быть добавлен в несколько коллекций, но в одну коллекцию может входить 1 раз",
    responses={
        HTTPStatus.OK: {"description": "Операция успешно выполнена"},
        HTTPStatus.CONFLICT: {
            "description": "Документ уже добавлен в коллекцию / "
                           "Документ для расчета TF не может быть пустым. Читать в теле ошибки"
        },

    }
)
async def add_collection_document(
        collection_id: UUID = Depends(validate_collection),
        document_id: UUID = Depends(validate_document),
        user: UserDTO = Depends(get_current_user),
        session: Session = Depends(get_session)
):
    try:
        collection_service = CollectionService(session)
        collection_service.move_document(collection_uuid=collection_id, document_uuid=document_id)
        collection_service.get_statistics(collection_uuid=collection_id, recount=True)
        return {"message": "Операция успешно выполнена"}
    except CollectionAlreadyHasDocumentException as hd:
        raise HTTPException(status_code=hd.status_code, detail=hd.message)
    except ValueError:
        raise HTTPException(status_code=HTTPStatus.CONFLICT, detail="The collection documents should not be empty")
