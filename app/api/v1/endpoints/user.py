from fastapi import APIRouter, Depends
from app.schema.auth_response import GetUserResponse
from app.model.models import User
from typing import Annotated
from app.core.dependencies import get_current_active_user


router = APIRouter(
    prefix="/users",
    tags=["user"]
)


@router.get("/me", response_model=GetUserResponse)
async def get_user(current_user: Annotated[User, Depends(get_current_active_user)]) -> GetUserResponse:
    return GetUserResponse.model_validate(current_user)


@router.get("/users/me/items/")
async def read_own_items(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    return [{"item_id": "Foo", "owner": current_user.username}]