from sqlalchemy import UUID, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.model.base_model import BaseModel
from app.model.post_model import Post
from app.core.enums import RoleEnum
from uuid import uuid4


class User(BaseModel):
    __tablename__ = "users"
    name: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(str, unique=True, nullable=False)
    password: Mapped[str]
    user_tocken: Mapped[uuid4] = mapped_column(UUID, unique=True, default=uuid4)
    is_active: Mapped[bool] = mapped_column(bool, default=True)
    role: Mapped[RoleEnum] = mapped_column(default=RoleEnum.User)

    post: Mapped[list[Post]] = relationship(
        "Post",
        back_populates="user"
    )
    