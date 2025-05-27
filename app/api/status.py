from fastapi import APIRouter

from app.services.app_service import AppService

router = APIRouter()

@router.get("/status")
async def get_status():
    status = AppService.check_status()
    return {"status": status}