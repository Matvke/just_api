from uuid import UUID
from app.repository import UserRepository
from app.model.models import User
from app.core.exceptions import NotFoundException


class UserService():
    def __init__(self, repository: UserRepository):
        self.repository = repository


    async def get_user_by_token(self, token: UUID) -> User:
        user = await self.repository.get_one_by_filters(user_token=token)
        if not user:
            raise NotFoundException(f"User with token {token} not found.") 
        return user
    

    async def get_user(self, username: str) -> User:
        user = await self.repository.get_one_by_filters(username=username)
        if not user:
            raise NotFoundException(f"User with username {username} not found.") 
        return user