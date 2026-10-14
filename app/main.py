from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from app.config import settings
from app.routers import system, services
from app.routers.objects import router as objects_router
from app.data.database import engine, Base

Base.metadata.create_all(bind=engine)

tags_metadata = [
    {"name": "System", "description": "Системные маршруты и статус приложения"},
    {"name": "Services", "description": "Операции с облачными сервисами"},
    {"name": "Objects", "description": "Операции с хранимыми объектами и файлами (ЛР 18)"},
]

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description=settings.app_description,
    debug=settings.debug,
    openapi_tags=tags_metadata
)


@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/docs")


app.include_router(system.router)
app.include_router(services.router)
app.include_router(objects_router)