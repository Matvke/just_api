from app.model.models import User
from .base_repository import BaseRepository


class UserRepository(BaseRepository[User]):
    @property
    def model(self) -> type[User]:
        return User
    
    