from sqlalchemy import DateTime
from sqlalchemy.dialects.postgresql import UUID, BOOLEAN
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base
from uuid import uuid4
from datetime import datetime, timezone
from sqlalchemy import String
from sqlalchemy.orm import relationship
from app.core.enums import RoleEnum
from sqlalchemy import ForeignKey


class BaseModel(Base):
    __abstract__ = True
    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, unique=True, default=uuid4)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))


class User(BaseModel):
    __tablename__ = "users"
    username: Mapped[str] = mapped_column(String(40))
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    user_token: Mapped[UUID] = mapped_column(UUID, unique=True, default=uuid4)
    role: Mapped[RoleEnum] = mapped_column(default=RoleEnum.User)
    is_active: Mapped[bool] = mapped_column(BOOLEAN, default=False)

    post: Mapped[list["Post"]] = relationship(
        "Post",
        back_populates="user",
        cascade= "all, delete-orphan"
    )


class Post(BaseModel):
    __tablename__ = "posts"
    title: Mapped[str] = mapped_column(String(255))
    content: Mapped[str] = mapped_column(String(1023))
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"))

    user: Mapped["User"] = relationship(
        "User",
        back_populates="post"
    )
    