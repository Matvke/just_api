from fastapi import APIRouter, Depends
from app.schema.security_schema import User
from typing import Annotated
from app.core.security import get_current_active_user


router = APIRouter(
    prefix="/users",
    tags=["user"]
)


@router.get("/me", response_model=User)
async def get_user(current_user: Annotated[User, Depends(get_current_active_user)]) -> User:
    return User.model_validate(current_user)
