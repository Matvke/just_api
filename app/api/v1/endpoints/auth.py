from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from app.core.dependencies import UserServiceDep
from app.core.security import fake_hash_password
from app.core.exceptions import NotFoundException

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)


@router.post("/token")
async def login(service: UserServiceDep, from_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    try:
        user = await service.get_user(from_data.username)
    except NotFoundException as e:
        raise HTTPException(status_code=400, detail=e.message)
    
    hashed_password = fake_hash_password(from_data.password)
    if not hashed_password == user.password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    return {"access_token": user.user_token, "token_type": "bearer"}

