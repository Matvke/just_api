from app.dependencies.repository_dependencies import UserRepositoryDep, PostRepositoryDep
from app.services.auth_service import AuthService
from app.services.user_service import UserService
from app.services.post_service import PostService
from typing import Annotated
from fastapi import Depends


async def get_auth_service(repository: UserRepositoryDep) -> AuthService:
    return AuthService(repository)
AuthServiceDep = Annotated[AuthService, Depends(get_auth_service)]


async def get_user_service(repository: UserRepositoryDep) -> UserService:
    return UserService(repository)
UserServiceDep = Annotated[UserService, Depends(get_user_service)]


async def get_post_service(repository: PostRepositoryDep) -> PostService:
    return PostService(repository)
PostServiceDep = Annotated[PostService, Depends(get_post_service)] 