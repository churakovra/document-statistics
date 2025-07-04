from http import HTTPStatus

from fastapi import APIRouter, UploadFile, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_session
from app.dependencies.auth import get_current_user
from app.enums.app_enums import HandlerTypes
from app.exceptions.collection_exceptions import BaseCollectionNotFoundException
from app.exceptions.document_exceptions import DocumentIsEmptyException, DocumentWrongTypeException
from app.schemas.document.document_upload_response import DocumentUploadResponse
from app.schemas.user.user_dto import UserDTO
from app.services.collection_service import CollectionService
from app.services.document_service import DocumentService

router = APIRouter()


@router.post(
    path="/documents/upload",
    tags=[HandlerTypes.DOCUMENTS],
    response_model=DocumentUploadResponse,
    status_code=HTTPStatus.OK,
    summary="Загрузка документа",
    description="Документы загружаются в базовую коллекцию пользователя. "
                "Если у пользователя нет базовой коллекции, она создается автоматически",
    responses={
        HTTPStatus.OK: {"description": "Документ успешно загружен"},
        HTTPStatus.CONFLICT: {"description": "Документ не может быть пустым"}
    }
)
async def upload_document(
        document: UploadFile,
        user: UserDTO = Depends(get_current_user),
        session: Session = Depends(get_session)
):
    document_service = DocumentService(session)
    try:
        document_service.validate_document(document.filename)
    except DocumentWrongTypeException as dwt:
        raise HTTPException(status_code=dwt.status_code, detail=dwt.message)

    collection_service = CollectionService(session)
    try:
        collection = collection_service.get_base_collection(user.uuid)
    except BaseCollectionNotFoundException:
        collection = collection_service.make_base_collection(user)

    try:
        new_doc_uuid = await document_service.upload_document(document, user)
    except DocumentIsEmptyException as de:
        raise HTTPException(status_code=de.status_code, detail=de.message)
    new_doc = document_service.get_document(document_uuid=new_doc_uuid, username=user.username)

    collection_service.add_document_to_base_collection(user, new_doc_uuid)
    return DocumentUploadResponse(collection=collection, document=new_doc)
