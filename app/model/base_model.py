from datetime import datetime, timezone
from sqlalchemy import UUID, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base
from uuid import uuid4


class BaseModel(Base):
    id: Mapped[uuid4] = mapped_column(UUID(as_uuid=True), primary_key=True, unique=True, default=uuid4)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
