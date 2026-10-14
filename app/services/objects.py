from pathlib import Path
from uuid import uuid4
from fastapi import UploadFile, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.config import settings
from app.data.models import StoredObject

def object_to_dict(obj: StoredObject) -> dict:
    return {
        "id": obj.id,
        "original_name": obj.original_name,
        "content_type": obj.content_type,
        "size_bytes": obj.size_bytes,
        "created_at": obj.created_at,
        "download_url": f"/objects/{obj.id}/download"
    }

async def save_object(db: Session, file: UploadFile) -> StoredObject:
    original_name = Path(file.filename or "file").name
    extension = Path(original_name).suffix.lower()
    storage_name = f"{uuid4().hex}{extension}"

    storage_directory = Path(settings.storage_path)
    storage_directory.mkdir(parents=True, exist_ok=True)
    file_path = storage_directory / storage_name

    size_bytes = 0
    max_size = settings.max_upload_size

    try:
        with file_path.open("wb") as buffer:
            while True:
                chunk = await file.read(1024 * 1024)
                if not chunk:
                    break
                size_bytes += len(chunk)
                if size_bytes > max_size:
                    raise HTTPException(
                        status_code=400,
                        detail=f"Размер файла превышает допустимый лимит {max_size // (1024 * 1024)} МБ"
                    )
                buffer.write(chunk)

        obj = StoredObject(
            original_name=original_name,
            storage_name=storage_name,
            content_type=file.content_type,
            size_bytes=size_bytes,
            storage_path=str(file_path)
        )
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj
    except Exception as e:
        db.rollback()
        if file_path.exists():
            file_path.unlink()
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=f"Ошибка сохранения файла: {str(e)}")
    finally:
        await file.close()

def get_objects(db: Session) -> list[StoredObject]:
    statement = select(StoredObject).order_by(StoredObject.id)
    return list(db.scalars(statement).all())

def get_object(db: Session, object_id: int) -> StoredObject | None:
    return db.get(StoredObject, object_id)

def delete_object(db: Session, obj: StoredObject) -> None:
    file_path = Path(obj.storage_path)
    if file_path.exists():
        file_path.unlink()
    db.delete(obj)
    db.commit()