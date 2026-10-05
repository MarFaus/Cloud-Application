from fastapi import APIRouter

router = APIRouter(prefix="/services", tags=["Services"])


@router.get("/")
def get_services():
    return [
        {"id": 1, "name": "Cloud Compute Service", "status": "active"},
        {"id": 2, "name": "Cloud Storage Service", "status": "active"}
    ]
