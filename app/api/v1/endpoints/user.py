from fastapi import APIRouter, Depends
from app.schemas import GetUserResponse
from app.model.models import User
from typing import Annotated
from app.dependencies.auth_dependencies import get_current_active_user


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.get("/me", response_model=GetUserResponse)
async def get_user(current_user: Annotated[User, Depends(get_current_active_user)]) -> GetUserResponse:
    return GetUserResponse.model_validate(current_user)