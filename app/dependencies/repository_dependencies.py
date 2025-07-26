from app.repository import UserRepository, PostRepository
from app.core.dependencies import SessionDep
from typing import Annotated
from fastapi import Depends


async def get_user_repository(session: SessionDep) -> UserRepository:
    return UserRepository(session)
UserRepositoryDep = Annotated[UserRepository, Depends(get_user_repository)]


async def get_post_repository(session: SessionDep) -> PostRepository:
    return PostRepository(session)
PostRepositoryDep = Annotated[PostRepository, Depends(get_post_repository)]