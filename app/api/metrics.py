from fastapi import APIRouter

from app.services.app_service import AppService

router = APIRouter()


@router.get("/metrics")
async def get_metrics():
    metrics = AppService.get_metrics()
    return metrics
