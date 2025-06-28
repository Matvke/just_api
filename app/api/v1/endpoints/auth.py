from fastapi import APIRouter
from app.schema.auth_schema import SignInResponse

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)


@router.post("sign_in", response_model=SignInResponse)
async def sign_in(user_info):
    ...
