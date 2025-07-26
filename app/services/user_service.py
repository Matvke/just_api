from uuid import UUID
from app.repository import UserRepository
from app.model.models import User
from app.exceptions.service_exceptions import NotFoundException


class UserService():
    def __init__(self, repository: UserRepository):
        self.repository = repository


    async def get_user_by_token(self, token: UUID) -> User:
        user = await self.repository.get_one_by_filters(user_token=token)
        if not user:
            raise NotFoundException(f"User with token {token} not found.") 
        return user
    

    async def get_user_by_username(self, username: str) -> User:
        user = await self.repository.get_one_by_filters(username=username)
        if not user:
            raise NotFoundException(f"User with username {username} not found.") 
        return user
    

    async def get_user_by_email(self, email: str) -> User:
        user = await self.repository.get_one_by_filters(email=email)
        if not user:
            raise NotFoundException(f"User with email {email} not found.")
        return user
    
