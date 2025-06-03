from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_session
from app.services.app_service import AppService

router = APIRouter()

@router.get("/status")
async def get_status(session: Session = Depends(get_session)):
    app_service = AppService(session)
    status = app_service.check_status()
    return {"status": status.value}