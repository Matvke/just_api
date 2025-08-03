from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app.dependencies.service_dependencies import AuthServiceDep
from app.core.security import ACCESS_TOKEN_EXPIRE_MINUTES
from app.schemas import SignUpRequest, GetUserResponse, Token
from app.exceptions import NotCreatedException, CredentialsException
from typing import Annotated
from datetime import timedelta


router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

@router.post("/token")
async def login_for_access_token(
    service: AuthServiceDep, 
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
    ) -> Token:
    user = await service.authenticate_user(form_data.username, form_data.password)
    
    if not user:
        raise CredentialsException(detail="Incorrect username or password")
    
    if user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = service.create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)

    return Token(access_token=access_token, token_type="bearer")


@router.post("/new", response_model=GetUserResponse)
async def sign_up(service: AuthServiceDep, form_data: SignUpRequest) -> GetUserResponse:
    try:
        user = await service.sign_up(form_data)
    except NotCreatedException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.message)
    
    return GetUserResponse.model_validate(user)