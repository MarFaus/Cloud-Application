from datetime import datetime
from pydantic import BaseModel

class StoredObjectResponse(BaseModel):
    id: int
    original_name: str
    content_type: str | None
    size_bytes: int
    created_at: datetime
    download_url: str

    class Config:
        from_attributes = True