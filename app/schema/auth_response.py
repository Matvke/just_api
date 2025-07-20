from pydantic import BaseModel, UUID4, ConfigDict
from app.core.enums import RoleEnum


class SignInResponse(BaseModel):
    user_token: UUID4
    role: RoleEnum

    model_config = ConfigDict(from_attributes=True)


class GetUserResponse(BaseModel):
    name: str
    email: str
    user_token: UUID4
    role: RoleEnum

    model_config = ConfigDict(from_attributes=True)
    