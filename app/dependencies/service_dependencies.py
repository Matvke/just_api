from app.dependencies.repository_dependencies import UserRepositoryDep
from app.services.auth_service import AuthService
from app.services.user_service import UserService
from typing import Annotated
from fastapi import Depends


async def get_auth_service(repository: UserRepositoryDep) -> AuthService:
    return AuthService(repository)
AuthServiceDep = Annotated[AuthService, Depends(get_auth_service)]


async def get_user_service(repository: UserRepositoryDep) -> UserService:
    return UserService(repository)
UserServiceDep = Annotated[UserService, Depends(get_user_service)]