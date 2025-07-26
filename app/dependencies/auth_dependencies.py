from typing import Annotated
from fastapi import Depends, HTTPException, status
from app.dependencies.service_dependencies import UserServiceDep
from app.core.security import oauth2_scheme, SECRET_KEY, ALGORITHM
from app.model.models import User
import jwt
from app.schemas.security_schema import TokenData
from jwt import InvalidTokenError



async def get_current_user( # TODO Нарушение границ слоев в get_current_user
        token: Annotated[str, Depends(oauth2_scheme)], 
        service: UserServiceDep
        ) -> User:
    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try: 
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM]) # это низкоуровневая техническая деталь. УБРАТЬ НА НИЖНИЙ СЛОЙ
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