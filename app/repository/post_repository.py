from app.model.models import Post
from .base_repository import BaseRepository


class PostRepository(BaseRepository[Post]):
    @property
    def model(self) -> type[Post]:
        return Post