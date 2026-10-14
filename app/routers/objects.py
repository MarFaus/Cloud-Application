from pathlib import Path
from typing import Annotated
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from app.data.database import get_db
from app.schemas.objects import StoredObjectResponse
from app.services.objects import (
    delete_object,
    get_object,
    get_objects,
    object_to_dict,
    save_object
)

router = APIRouter(prefix="/objects", tags=["Objects"])

@router.post("", response_model=StoredObjectResponse, status_code=201, summary="Загрузить объект")
async def upload_object(
    file: Annotated[UploadFile, File(description="Файл для сохранения в объектном хранилище")],
    db: Session = Depends(get_db)
):
    obj = await save_object(db, file)
    return object_to_dict(obj)

@router.get("", response_model=list[StoredObjectResponse], summary="Получить список объектов")
def read_objects(db: Session = Depends(get_db)):
    objects = get_objects(db)
    return [object_to_dict(obj) for obj in objects]

@router.get("/{object_id}", response_model=StoredObjectResponse, summary="Получить сведения об объекте")
def read_object(object_id: int, db: Session = Depends(get_db)):
    obj = get_object(db, object_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="Object not found")
    return object_to_dict(obj)

@router.get("/{object_id}/download", summary="Скачать объект")
def download_object(object_id: int, db: Session = Depends(get_db)):
    obj = get_object(db, object_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="Object not found")
    file_path = Path(obj.storage_path)
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Stored file not found")
    return FileResponse(
        path=str(file_path),
        media_type=obj.content_type or "application/octet-stream",
        filename=obj.original_name
    )

@router.delete("/{object_id}", summary="Удалить объект")
def remove_object(object_id: int, db: Session = Depends(get_db)):
    obj = get_object(db, object_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="Object not found")
    delete_object(db, obj)
    return {"message": "Object deleted", "id": object_id}