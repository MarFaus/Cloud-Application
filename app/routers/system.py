from fastapi import APIRouter
from app.config import settings

router = APIRouter(tags=["System"])


@router.get("/status")
def status():
    return {
        "status": "ok",
        "application": settings.app_name,
        "version": settings.app_version,
        "environment": settings.app_env,
        "debug": settings.debug,
        "api_prefix": settings.api_prefix
    }
