from typing import Annotated
from fastapi import Depends, HTTPException, status
from app.dependencies.service_dependencies import AuthServiceDep
from app.core.security import oauth2_scheme
from app.model.models import User
from app.exceptions import NotFoundException, InvalidCredentialsException, CredentialsException
from app.core.enums import RoleEnum



async def get_current_user(
        token: Annotated[str, Depends(oauth2_scheme)], 
        service: AuthServiceDep
        ) -> User:

    try: 
        user = await service.get_user_from_token(token)

    except NotFoundException | InvalidCredentialsException:
        raise CredentialsException()

    return user


async def get_current_active_user(current_user: Annotated[User, Depends(get_current_user)]):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
GetCurrUserDep = Annotated[User, Depends(get_current_active_user)]


async def get_current_active_admin(current_user: Annotated[User, Depends(get_current_user)]):
    if current_user.disabled:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")
    if current_user.role != RoleEnum.Admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User isn't admin")
    return current_user
GetCurrAdminDep = Annotated[User, Depends(get_current_active_admin)]