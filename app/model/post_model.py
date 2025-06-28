from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.model.base_model import BaseModel
from app.model.user_model import User

class Post(BaseModel):
    __tablename__ = "posts"
    title: Mapped[str] = mapped_column(String(255))
    content: Mapped[str] = mapped_column(String(1023))
    is_active: Mapped[bool] = mapped_column(bool, default=True)

    user: Mapped[User] = relationship(
        "User",
        back_populates="post"
    )
    