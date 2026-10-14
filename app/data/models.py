from datetime import datetime
from sqlalchemy import Integer, String, BigInteger, DateTime, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column
from app.data.database import Base

class StoredObject(Base):
    __tablename__ = "stored_objects"
    __table_args__ = (
        UniqueConstraint("storage_name", name="uq_stored_objects_storage_name"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    original_name: Mapped[str] = mapped_column(String(255), nullable=False)
    storage_name: Mapped[str] = mapped_column(String(255), nullable=False)
    content_type: Mapped[str | None] = mapped_column(String(100), nullable=True)
    size_bytes: Mapped[int] = mapped_column(BigInteger, nullable=False)
    storage_path: Mapped[str] = mapped_column(String(500), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        server_default=func.now(),
        nullable=False
    )