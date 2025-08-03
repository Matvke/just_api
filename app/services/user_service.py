from uuid import UUID
from app.repository import UserRepository
from app.model.models import User
from app.exceptions.service_exceptions import NotFoundException
from app.core.enums import RoleEnum


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
    

    async def set_role(self, id: UUID, role: RoleEnum) -> User:
        try:
            user = await self.repository.update_attr(id=id, column='role', value=role)
            await self.repository.session.commit()
        except Exception as e:
            await self.repository.session.rollback()
            raise e
        if not user:
            raise NotFoundException(f"User with id {id} not found.")
        return user 
    

    async def soft_delete_user(self, id: UUID) -> None:
        try:
            await self.repository.soft_delete(id=id)
            await self.repository.session.commit()
        except Exception as e:
            await self.repository.session.rollback()
            raise e
        
    
    async def restore_user(self, id: UUID) -> None:
        try:
            await self.repository.soft_delete(id=id)
            await self.repository.session.commit()
        except Exception as e:
            await self.repository.session.rollback()
            raise e