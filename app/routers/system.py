from fastapi import APIRouter, Request

router = APIRouter(tags=["System"])

@router.get("/connection", summary="Информация о соединении")
def connection_info(request: Request):
    return {
        "scheme": request.url.scheme,
        "host": request.url.hostname,
        "secure": (request.url.scheme == "https")
    }
