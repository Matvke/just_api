from fastapi.security import OAuth2PasswordBearer
from fastapi import status
from typing import Annotated
from fastapi import Depends, HTTPException
from app.schema.security_schema import User
from .dependencies import UserServiceDep


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token")


async def fake_decode_token(token, service: UserServiceDep):
    user = await service.get_user_by_token(token)
    return User.model_validate(user)

def fake_hash_password(password: str):
    return password


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], service: UserServiceDep):
    user = await fake_decode_token(token, service)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


async def get_current_active_user(current_user: Annotated[User, Depends(get_current_user)]):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user