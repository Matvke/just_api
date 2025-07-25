from .database import async_session_factory
from sqlalchemy.ext.asyncio import AsyncSession
from typing import AsyncGenerator, Annotated
from fastapi import Depends, HTTPException, status
from app.repository import UserRepository, PostRepository
from app.services.auth_service import AuthService 
from app.services.user_service import UserService
from app.schema.security_schema import TokenData
from app.model.models import User
from jwt.exceptions import InvalidTokenError
from app.core.security import SECRET_KEY, ALGORITHM, oauth2_scheme
import jwt


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


async def get_current_user(
        token: Annotated[str, Depends(oauth2_scheme)], 
        service: UserServiceDep
        ) -> User:
    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
        
    except InvalidTokenError:
        raise credentials_exception
    user = await service.get_user_by_username(username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: Annotated[User, Depends(get_current_user)]):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user