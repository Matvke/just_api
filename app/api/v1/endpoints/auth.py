from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from app.core.dependencies import UserServiceDep
from app.core.security import Token, authenticate_user, create_access_token
from datetime import timedelta

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

ACCESS_TOKEN_EXPIRE_MINUTES = 30

@router.post("/token")
async def login_for_access_token(
    service: UserServiceDep, 
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
    ) -> Token:
    user = await authenticate_user(form_data.username, form_data.password, service)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub":user.username}, expires_delta=access_token_expires)
    return Token(access_token=access_token, token_type="bearer")