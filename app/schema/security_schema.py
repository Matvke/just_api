from pydantic import BaseModel, EmailStr, ConfigDict


class User(BaseModel):
    username: str
    email: EmailStr
    is_active: bool
    password: str

    model_config = ConfigDict(from_attributes=True)