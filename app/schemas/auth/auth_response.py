from pydantic import BaseModel, UUID4, ConfigDict, EmailStr
from app.core.enums import RoleEnum


class SignInResponse(BaseModel):
    user_token: UUID4
    role: RoleEnum

    model_config = ConfigDict(from_attributes=True)


class GetUserResponse(BaseModel):
    id: UUID4
    username: str
    email: EmailStr
    disabled: bool
    model_config = ConfigDict(from_attributes=True)
    