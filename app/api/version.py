from fastapi import APIRouter

from app.services.app_service import AppService

router = APIRouter()

@router.get("/version")
async def get_version():
    version = AppService.get_version()
    return {"version": version}