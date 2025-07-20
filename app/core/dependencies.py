from .database import async_session_factory
from sqlalchemy.ext.asyncio import AsyncSession
from typing import AsyncGenerator, Annotated
from fastapi import Depends
from app.repository import UserRepository, PostRepository
from app.services.auth_service import AuthService 
from app.services.user_service import UserService


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_factory() as session:
        yield session
SessionDep = Annotated[AsyncSession, Depends(get_session)]


async def get_user_repository(session: SessionDep) -> UserRepository:
    return UserRepository(session)
UserRepositoryDep = Annotated[UserRepository, Depends(get_user_repository)]


async def get_post_repository(session: SessionDep) -> PostRepository:
    return PostRepository(session)
PostRepositoryDep = Annotated[PostRepository, Depends(get_post_repository)]


async def get_auth_service(repository: UserRepositoryDep) -> AuthService:
    return AuthService(repository)
AuthServiceDep = Annotated[AuthService, Depends(get_auth_service)]


async def get_user_service(repository: UserRepositoryDep) -> UserService:
    return UserService(repository)
UserServiceDep = Annotated[UserService, Depends(get_user_service)]